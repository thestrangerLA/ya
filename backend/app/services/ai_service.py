"""
AI Assistant service — local semantic search engine.

Architecture:
    1. Parse user query into keywords and detect animal type mentions.
    2. Score diseases by keyword overlap with symptoms, name, cause, treatment.
    3. Collect all recommended medicines from matched diseases.
    4. Return ranked results with no hallucination — only DB records.
"""

import re
import uuid
from dataclasses import dataclass, field
from typing import List, Optional, Set, Tuple

from sqlalchemy import or_, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from app.models.models import AnimalType, Disease, Medicine, MedicineImage
from app.schemas.schemas import (
    AIMatchedDisease,
    AIRecommendedMedicine,
    AIResponse,
)

# ── Stop words to ignore during keyword extraction ─────────────────────────
STOP_WORDS: Set[str] = {
    "my", "the", "a", "an", "is", "are", "was", "were", "be", "been",
    "being", "have", "has", "had", "do", "does", "did", "will", "would",
    "could", "should", "may", "might", "shall", "can", "it", "its",
    "this", "that", "these", "those", "and", "or", "but", "if", "in",
    "on", "at", "to", "for", "of", "with", "by", "from", "as", "into",
    "what", "which", "who", "whom", "how", "when", "where", "why",
    "he", "she", "they", "we", "i", "you", "your", "their", "our",
    "chicken", "dog", "cat", "pig", "goat", "sheep", "cattle", "fish", "bird",
    "fighting",
}

ANIMAL_KEYWORDS: dict[str, str] = {
    "chicken": "Chicken",
    "hen": "Chicken",
    "rooster": "Chicken",
    "chick": "Chicken",
    "poultry": "Chicken",
    "fighting chicken": "Fighting Chicken",
    "gamecock": "Fighting Chicken",
    "cow": "Cattle",
    "cattle": "Cattle",
    "bull": "Cattle",
    "calf": "Cattle",
    "pig": "Pig",
    "hog": "Pig",
    "swine": "Pig",
    "pork": "Pig",
    "goat": "Goat",
    "sheep": "Sheep",
    "lamb": "Sheep",
    "dog": "Dog",
    "puppy": "Dog",
    "canine": "Dog",
    "cat": "Cat",
    "kitten": "Cat",
    "feline": "Cat",
    "fish": "Fish",
    "bird": "Bird",
    "parrot": "Bird",
    "duck": "Bird",
}


def _extract_keywords(query: str) -> Tuple[List[str], Optional[str]]:
    """Extract meaningful keywords and detect animal type from query."""
    lower = query.lower()

    # Detect animal type from query
    detected_animal: Optional[str] = None
    for keyword, animal_name in ANIMAL_KEYWORDS.items():
        if keyword in lower:
            detected_animal = animal_name
            break

    # Tokenize and filter stop words
    tokens = re.findall(r"\b[a-zA-Z]{2,}\b", lower)
    keywords = [t for t in tokens if t not in STOP_WORDS]
    return keywords, detected_animal


def _score_disease(disease: Disease, keywords: List[str]) -> Tuple[float, List[str]]:
    """
    Score a disease record based on keyword overlap.
    Returns (score, matched_keywords).
    """
    searchable_text = " ".join(filter(None, [
        disease.name,
        disease.symptoms,
        disease.cause,
        disease.treatment,
        disease.prevention,
    ])).lower()

    matched = [kw for kw in keywords if kw in searchable_text]
    if not keywords:
        return 0.0, []

    # Weighted scoring: symptom matches count more
    score = 0.0
    symptom_text = (disease.symptoms or "").lower()
    for kw in matched:
        if kw in symptom_text:
            score += 1.5  # symptom match is stronger
        elif kw in (disease.name or "").lower():
            score += 1.2  # name match
        else:
            score += 1.0

    normalized = min(score / (len(keywords) * 1.5), 1.0)
    return round(normalized, 3), matched


def _build_image_url(image: MedicineImage, base_url: str = "") -> str:
    return f"{base_url}/api/v1/files/{image.file_path}"


async def ai_search(
    db: AsyncSession,
    query: str,
    animal_type_id: Optional[uuid.UUID] = None,
    base_url: str = "",
) -> AIResponse:
    """
    Main AI search function.
    Matches the user's natural-language query to diseases and medicines
    in the local database. Never invents information.
    """
    keywords, detected_animal = _extract_keywords(query)

    # Resolve animal type filter
    effective_animal_type_id = animal_type_id
    if not effective_animal_type_id and detected_animal:
        result = await db.execute(
            select(AnimalType).where(AnimalType.name == detected_animal)
        )
        animal_type = result.scalar_one_or_none()
        if animal_type:
            effective_animal_type_id = animal_type.id

    # ── Load diseases ─────────────────────────────────────────────────────
    disease_query = select(Disease).options(
        selectinload(Disease.animal_type),
        selectinload(Disease.recommended_medicines).selectinload(Medicine.images),
        selectinload(Disease.recommended_medicines).selectinload(Medicine.animal_type),
    )
    if effective_animal_type_id:
        disease_query = disease_query.where(
            Disease.animal_type_id == effective_animal_type_id
        )
    diseases_result = await db.execute(disease_query)
    all_diseases = list(diseases_result.scalars().all())

    # ── Score and rank diseases ───────────────────────────────────────────
    scored: List[Tuple[float, Disease, List[str]]] = []
    for disease in all_diseases:
        score, matched = _score_disease(disease, keywords)
        if score > 0 or not keywords:
            scored.append((score, disease, matched))

    # Sort by score descending, take top 5
    scored.sort(key=lambda x: x[0], reverse=True)
    top_diseases = scored[:5]

    # ── Build response ────────────────────────────────────────────────────
    seen_medicine_ids: Set[uuid.UUID] = set()
    all_medicines: List[AIRecommendedMedicine] = []
    matched_diseases: List[AIMatchedDisease] = []

    for score, disease, matched_kws in top_diseases:
        rec_medicines = []
        for med in disease.recommended_medicines:
            primary_url = None
            if med.images:
                primary = next((img for img in med.images if img.is_primary), med.images[0])
                primary_url = _build_image_url(primary, base_url)

            med_schema = AIRecommendedMedicine(
                id=med.id,
                name=med.name,
                brand=med.brand,
                dosage=med.dosage,
                warnings=med.warnings,
                stock_quantity=med.stock_quantity,
                primary_image_url=primary_url,
            )
            rec_medicines.append(med_schema)

            if med.id not in seen_medicine_ids:
                seen_medicine_ids.add(med.id)
                all_medicines.append(med_schema)

        matched_diseases.append(
            AIMatchedDisease(
                id=disease.id,
                name=disease.name,
                symptoms=disease.symptoms,
                treatment=disease.treatment,
                animal_type_name=disease.animal_type.name if disease.animal_type else None,
                recommended_medicines=rec_medicines,
                match_score=score,
                matched_keywords=matched_kws,
            )
        )

    # ── Interpretation text ───────────────────────────────────────────────
    if detected_animal:
        interpretation = f"Searching for {detected_animal}-related conditions matching: {', '.join(keywords) or query}"
    else:
        interpretation = f"Searching all animal conditions matching: {', '.join(keywords) or query}"

    if not matched_diseases:
        interpretation += ". No matching records found in the database."

    return AIResponse(
        query=query,
        interpretation=interpretation,
        possible_diseases=matched_diseases,
        all_recommended_medicines=all_medicines,
    )
