"""
Database seed script.

Populates the database with:
  - 10 Animal Types
  - 8 Medicine Categories
  - 15 Sample Medicines
  - 10 Sample Diseases with recommended medicines

Run: python seed.py  (from backend/ directory with .env loaded)
"""

import asyncio
import sys
import os
from datetime import date, timedelta

# Add backend dir to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import AsyncSessionLocal, engine, Base
from app.models.models import AnimalType, Category, Medicine, Disease


# ── Seed Data ──────────────────────────────────────────────────────────────

ANIMAL_TYPES = [
    {"name": "Chicken", "icon": "🐔", "description": "Domestic poultry including broilers and layers"},
    {"name": "Fighting Chicken", "icon": "🐓", "description": "Gamefowl raised for strength and conditioning"},
    {"name": "Cattle", "icon": "🐄", "description": "Bovine livestock including cows, bulls, and calves"},
    {"name": "Pig", "icon": "🐷", "description": "Swine livestock for meat and breeding"},
    {"name": "Goat", "icon": "🐐", "description": "Small ruminant livestock"},
    {"name": "Sheep", "icon": "🐑", "description": "Wool and meat producing livestock"},
    {"name": "Dog", "icon": "🐕", "description": "Domestic canine companion and working animal"},
    {"name": "Cat", "icon": "🐈", "description": "Domestic feline companion animal"},
    {"name": "Fish", "icon": "🐟", "description": "Aquatic animals including tilapia, milkfish, and ornamental fish"},
    {"name": "Bird", "icon": "🦜", "description": "Avian animals including parrots, ducks, and ornamental birds"},
]

CATEGORIES = [
    {"name": "Antibiotic", "description": "Medicines that kill or inhibit bacterial infections"},
    {"name": "Antiparasitic", "description": "Medicines against internal and external parasites"},
    {"name": "Antiviral", "description": "Medicines that combat viral infections"},
    {"name": "Vaccine", "description": "Preventive biological preparations"},
    {"name": "Anti-inflammatory", "description": "Medicines that reduce inflammation and fever"},
    {"name": "Vitamin & Supplement", "description": "Nutritional supplements and vitamins"},
    {"name": "Antifungal", "description": "Medicines that treat fungal infections"},
    {"name": "Disinfectant", "description": "Topical antiseptics and disinfectants"},
]

MEDICINES_DATA = [
    {
        "name": "Oxytetracycline 20%",
        "brand": "TerraVet",
        "sku": "TV-OXY-001",
        "animal": "Chicken",
        "category": "Antibiotic",
        "description": "Broad-spectrum antibiotic for treatment of bacterial infections in poultry",
        "indications": "Respiratory infections, CRD (Chronic Respiratory Disease), Fowl Cholera, Infectious Coryza",
        "dosage": "10–20 mg/kg body weight per day for 3–5 days",
        "usage": "Dissolve in drinking water. Administer fresh solution daily.",
        "warnings": "Withdraw 5 days before slaughter. Do not use in laying hens producing eggs for human consumption.",
        "side_effects": "May cause gastrointestinal upset. Overuse may lead to antibiotic resistance.",
        "storage": "Store below 25°C in a dry place, away from light.",
        "stock_quantity": 150,
        "price": 285.00,
        "expiration_date": date.today() + timedelta(days=365),
    },
    {
        "name": "Amoxicillin 15%",
        "brand": "AmoxiPet",
        "sku": "AP-AMX-002",
        "animal": "Dog",
        "category": "Antibiotic",
        "description": "Broad-spectrum penicillin antibiotic for dogs and cats",
        "indications": "Skin infections, respiratory tract infections, urinary tract infections, dental infections",
        "dosage": "10–20 mg/kg twice daily for 5–7 days",
        "usage": "Oral administration with or without food.",
        "warnings": "Do not use in animals with known hypersensitivity to penicillins.",
        "side_effects": "Vomiting, diarrhea, allergic reactions (rare)",
        "storage": "Store in cool, dry place below 30°C.",
        "stock_quantity": 80,
        "price": 420.00,
        "expiration_date": date.today() + timedelta(days=240),
    },
    {
        "name": "Ivermectin 1%",
        "brand": "IverCare",
        "sku": "IC-IVM-003",
        "animal": "Cattle",
        "category": "Antiparasitic",
        "description": "Broad-spectrum antiparasitic for treatment of internal and external parasites in cattle",
        "indications": "Roundworms, lungworms, lice, mange mites, ticks",
        "dosage": "200 mcg/kg body weight subcutaneously",
        "usage": "Subcutaneous injection under the skin of the neck region.",
        "warnings": "Do not use in dairy cattle producing milk for human consumption. 49-day withdrawal period for meat.",
        "side_effects": "Mild swelling at injection site. Lethargy may occur.",
        "storage": "Store at 15–30°C. Protect from light.",
        "stock_quantity": 60,
        "price": 650.00,
        "expiration_date": date.today() + timedelta(days=180),
    },
    {
        "name": "Newcastle Disease Vaccine (La Sota)",
        "brand": "PoultryShield",
        "sku": "PS-NDV-004",
        "animal": "Chicken",
        "category": "Vaccine",
        "description": "Live attenuated vaccine for prevention of Newcastle Disease in poultry",
        "indications": "Prevention of Newcastle Disease (Avian paramyxovirus type 1)",
        "dosage": "1 dose per bird via drinking water or eye drop",
        "usage": "Drinking water method: dissolve in clean water. Eye drop: 1–2 drops per eye.",
        "warnings": "Do not vaccinate sick birds. Use within 2 hours of reconstitution.",
        "side_effects": "Mild respiratory symptoms (1–3 days) normal post-vaccination reaction",
        "storage": "Store at 2–8°C. Keep frozen if stored long-term. Do not freeze reconstituted vaccine.",
        "stock_quantity": 500,
        "price": 150.00,
        "expiration_date": date.today() + timedelta(days=90),
    },
    {
        "name": "Albendazole 10%",
        "brand": "AlbaSure",
        "sku": "AS-ALB-005",
        "animal": "Goat",
        "category": "Antiparasitic",
        "description": "Anthelmintic for treatment of gastrointestinal roundworms and tapeworms in goats and sheep",
        "indications": "Haemonchus, Ostertagia, Trichostrongylus, Fasciola hepatica (liver fluke)",
        "dosage": "7.5 mg/kg for roundworms; 15 mg/kg for liver fluke. Oral.",
        "usage": "Administer orally using a drenching gun.",
        "warnings": "Do not use in early pregnancy (first 45 days). 10-day meat withdrawal.",
        "side_effects": "Generally well tolerated. Occasional drooling.",
        "storage": "Store at room temperature away from direct sunlight.",
        "stock_quantity": 8,  # Low stock!
        "price": 320.00,
        "expiration_date": date.today() + timedelta(days=300),
    },
    {
        "name": "Enrofloxacin 10%",
        "brand": "EnroVet",
        "sku": "EV-ENR-006",
        "animal": "Pig",
        "category": "Antibiotic",
        "description": "Fluoroquinolone antibiotic for treatment of bacterial infections in swine",
        "indications": "Swine respiratory disease, MMA (mastitis-metritis-agalactia), colibacillosis",
        "dosage": "2.5 mg/kg body weight once daily for 3 days",
        "usage": "Intramuscular injection in neck muscle.",
        "warnings": "Do not use in breeding animals. 10-day withdrawal period.",
        "side_effects": "Local tissue reaction at injection site.",
        "storage": "Store at 15–25°C protected from light.",
        "stock_quantity": 45,
        "price": 890.00,
        "expiration_date": date.today() + timedelta(days=20),  # Expiring soon!
    },
    {
        "name": "Vitamin B-Complex Injection",
        "brand": "VitaFarm",
        "sku": "VF-VBC-007",
        "animal": "Cattle",
        "category": "Vitamin & Supplement",
        "description": "Injectable B-vitamin complex for nutritional support in cattle and livestock",
        "indications": "B-vitamin deficiency, appetite loss, stress recovery, post-illness support",
        "dosage": "5–10 mL intramuscularly or subcutaneously, repeat in 3–5 days if needed",
        "usage": "Intramuscular or subcutaneous injection.",
        "warnings": "Anaphylactic reactions possible. Have epinephrine available.",
        "side_effects": "Mild pain at injection site.",
        "storage": "Store at 15–25°C. Protect from light and freezing.",
        "stock_quantity": 120,
        "price": 195.00,
        "expiration_date": date.today() + timedelta(days=400),
    },
    {
        "name": "Tylosin 20% Soluble Powder",
        "brand": "TyloFarm",
        "sku": "TF-TYL-008",
        "animal": "Chicken",
        "category": "Antibiotic",
        "description": "Macrolide antibiotic for treatment of mycoplasmosis and related respiratory conditions in poultry",
        "indications": "Mycoplasmosis (CRD), Infectious Synovitis, Bordetellosis",
        "dosage": "500 mg per liter of drinking water for 3–5 days",
        "usage": "Dissolve in drinking water. Use fresh solution daily.",
        "warnings": "5-day withdrawal for meat. Not for use in laying hens.",
        "side_effects": "Reduced feed intake (mild, temporary).",
        "storage": "Store in cool, dry place below 25°C.",
        "stock_quantity": 6,  # Low stock!
        "price": 375.00,
        "expiration_date": date.today() + timedelta(days=200),
    },
    {
        "name": "Fenbendazole 10% Suspension",
        "brand": "FenzoVet",
        "sku": "FV-FBZ-009",
        "animal": "Dog",
        "category": "Antiparasitic",
        "description": "Broad-spectrum anthelmintic for dogs and cats",
        "indications": "Roundworms (Toxocara), hookworms (Ancylostoma), whipworms (Trichuris), tapeworms (Taenia)",
        "dosage": "50 mg/kg once daily for 3 consecutive days",
        "usage": "Mix with food or administer orally with syringe.",
        "warnings": "Not for use in puppies under 6 weeks.",
        "side_effects": "Vomiting or diarrhea (rare).",
        "storage": "Store at room temperature. Shake well before use.",
        "stock_quantity": 55,
        "price": 280.00,
        "expiration_date": date.today() + timedelta(days=350),
    },
    {
        "name": "Povidone Iodine 10% Solution",
        "brand": "IodoCare",
        "sku": "IC-PVI-010",
        "animal": "Pig",
        "category": "Disinfectant",
        "description": "Topical antiseptic for wound care and surgical site preparation in all livestock",
        "indications": "Wound disinfection, navel care in newborns, skin infections, surgical preparation",
        "dosage": "Apply undiluted or diluted 1:10 with water to affected area",
        "usage": "Clean area first, apply with cotton swab or spray. Repeat twice daily.",
        "warnings": "Avoid contact with eyes. Do not use on deep puncture wounds without vet guidance.",
        "side_effects": "Skin staining (temporary). Rare iodine sensitivity.",
        "storage": "Store at room temperature away from heat and light.",
        "stock_quantity": 200,
        "price": 120.00,
        "expiration_date": date.today() + timedelta(days=500),
    },
    {
        "name": "Dexamethasone 0.2% Injection",
        "brand": "DexaVet",
        "sku": "DV-DEX-011",
        "animal": "Cattle",
        "category": "Anti-inflammatory",
        "description": "Corticosteroid for treatment of inflammation and allergic reactions in cattle",
        "indications": "Allergic reactions, inflammation, shock, ketosis adjunct therapy",
        "dosage": "0.04–0.08 mg/kg IV or IM once, repeat as needed",
        "usage": "Intravenous or intramuscular injection by veterinarian.",
        "warnings": "Long-term use may suppress immune system. Do not use in pregnant animals (may induce parturition).",
        "side_effects": "Polyuria, polydipsia, immune suppression with prolonged use.",
        "storage": "Store at 15–25°C. Protect from light.",
        "stock_quantity": 35,
        "price": 550.00,
        "expiration_date": date.today() + timedelta(days=25),  # Expiring soon!
    },
    {
        "name": "Marek's Disease Vaccine",
        "brand": "MarekShield",
        "sku": "MS-MDV-012",
        "animal": "Chicken",
        "category": "Vaccine",
        "description": "Cell-associated vaccine for prevention of Marek's Disease in day-old chicks",
        "indications": "Prevention of Marek's Disease (Herpesvirus of turkeys strain)",
        "dosage": "0.2 mL per chick subcutaneously at day-old",
        "usage": "Subcutaneous injection in neck. Administer at hatchery.",
        "warnings": "Store in liquid nitrogen. Thaw in 25–27°C water bath immediately before use.",
        "side_effects": "Mild swelling at injection site.",
        "storage": "Store in liquid nitrogen (-196°C). Extremely cold-chain sensitive.",
        "stock_quantity": 1000,
        "price": 8.50,
        "expiration_date": date.today() + timedelta(days=60),
    },
    {
        "name": "Fluconazole Oral Solution 2%",
        "brand": "FlucoVet",
        "sku": "FV-FLC-013",
        "animal": "Bird",
        "category": "Antifungal",
        "description": "Antifungal medication for treatment of Aspergillosis and Candidiasis in birds",
        "indications": "Aspergillosis, Candidiasis, Cryptococcosis in avian species",
        "dosage": "5–10 mg/kg body weight daily for 14–21 days",
        "usage": "Oral administration directly or mixed with soft food.",
        "warnings": "Use with caution in birds with liver disease.",
        "side_effects": "Anorexia, vomiting (rare).",
        "storage": "Store at room temperature. Keep container tightly closed.",
        "stock_quantity": 25,
        "price": 460.00,
        "expiration_date": date.today() + timedelta(days=270),
    },
    {
        "name": "Praziquantel Tablet 50mg",
        "brand": "PraziPet",
        "sku": "PP-PRZ-014",
        "animal": "Cat",
        "category": "Antiparasitic",
        "description": "Cestocide for treatment of tapeworm infections in cats and dogs",
        "indications": "Dipylidium caninum, Taenia taeniaeformis, Echinococcus tapeworms",
        "dosage": "5 mg/kg for cats; 2.5–5 mg/kg for dogs",
        "usage": "Oral tablet with or without food. May be crushed and mixed with food.",
        "warnings": "Not for kittens under 4 weeks.",
        "side_effects": "Salivation, vomiting (rare).",
        "storage": "Store below 30°C away from moisture.",
        "stock_quantity": 9,  # Low stock!
        "price": 65.00,
        "expiration_date": date.today() + timedelta(days=400),
    },
    {
        "name": "Tilapia Antibiotic Premix",
        "brand": "AquaVet",
        "sku": "AV-TAP-015",
        "animal": "Fish",
        "category": "Antibiotic",
        "description": "Medicated feed premix for treatment of bacterial infections in tilapia and other aquaculture fish",
        "indications": "Columnaris disease, Aeromoniasis, Streptococcosis in aquaculture",
        "dosage": "Mix 10g per kg of fish feed. Feed for 7–10 days.",
        "usage": "Mix thoroughly into fish feed. Feed as normal daily ration.",
        "warnings": "30-day withdrawal before harvest. Avoid overuse to prevent resistance.",
        "side_effects": "Temporary reduction in feed intake.",
        "storage": "Store in cool, dry place below 25°C. Keep sealed.",
        "stock_quantity": 75,
        "price": 540.00,
        "expiration_date": date.today() + timedelta(days=180),
    },
]

DISEASES_DATA = [
    {
        "name": "Newcastle Disease",
        "animal": "Chicken",
        "symptoms": "Coughing, sneezing, twisted neck (torticollis), greenish diarrhea, sudden death, drooping wings, respiratory distress, decreased egg production",
        "cause": "Newcastle disease virus (NDV), an avian paramyxovirus. Highly contagious. Spread through secretions, feces, contaminated equipment.",
        "prevention": "Vaccination with La Sota or HB1 strains. Strict biosecurity. Quarantine new birds. Clean and disinfect housing regularly.",
        "treatment": "No specific antiviral treatment. Supportive care: electrolytes, vitamins. Secondary bacterial infections treated with antibiotics.",
        "medicines": ["Newcastle Disease Vaccine (La Sota)", "Oxytetracycline 20%"],
    },
    {
        "name": "Chronic Respiratory Disease (CRD)",
        "animal": "Chicken",
        "symptoms": "Coughing, sneezing, nasal discharge, rattling breathing sounds, conjunctivitis, reduced feed intake, weight loss",
        "cause": "Mycoplasma gallisepticum bacteria. Often complicated by secondary infections (E. coli, Newcastle). Stress, poor ventilation worsen condition.",
        "prevention": "Use Mycoplasma-free stock. Maintain good ventilation. All-in/all-out management. Avoid overcrowding.",
        "treatment": "Tylosin, Oxytetracycline, or Enrofloxacin in drinking water. Improve ventilation. Vitamin supplementation.",
        "medicines": ["Tylosin 20% Soluble Powder", "Oxytetracycline 20%"],
    },
    {
        "name": "Marek's Disease",
        "animal": "Chicken",
        "symptoms": "Leg or wing paralysis, vision impairment (gray eye), tumors in organs, skin lesions around feather follicles, sudden death",
        "cause": "Marek's Disease Virus (MDV), a herpesvirus. Highly contagious via feather dander. No treatment once infected.",
        "prevention": "Vaccination at day-old with HVT or bivalent vaccine. Strict biosecurity.",
        "treatment": "No effective treatment. Prevent through vaccination.",
        "medicines": ["Marek's Disease Vaccine"],
    },
    {
        "name": "Parvovirus Infection (Dogs)",
        "animal": "Dog",
        "symptoms": "Severe bloody diarrhea, vomiting, lethargy, loss of appetite, fever, dehydration, abdominal pain",
        "cause": "Canine Parvovirus Type 2 (CPV-2). Highly contagious. Survives in environment for months. Spread through feces.",
        "prevention": "Regular vaccination (core vaccine). Minimize contact with infected dogs. Disinfect with bleach solution.",
        "treatment": "Supportive care: IV fluids, antiemetics, antibiotics for secondary infections. Hospitalization required.",
        "medicines": ["Amoxicillin 15%", "Vitamin B-Complex Injection"],
    },
    {
        "name": "Canine Distemper",
        "animal": "Dog",
        "symptoms": "Fever, nasal discharge, coughing, vomiting, diarrhea, seizures, hardened paw pads (hard pad disease), neurological signs",
        "cause": "Canine Distemper Virus (CDV), a morbillivirus. Airborne transmission. Affects respiratory, GI, and nervous systems.",
        "prevention": "Vaccination (core vaccine, part of DHPP combo). Avoid contact with wildlife.",
        "treatment": "Supportive care: antibiotics for secondary infections, anticonvulsants for seizures, IV fluids.",
        "medicines": ["Amoxicillin 15%"],
    },
    {
        "name": "Intestinal Worm Infestation (Dogs)",
        "animal": "Dog",
        "symptoms": "Weight loss despite good appetite, pot-belly appearance, diarrhea or constipation, visible worms in feces, vomiting, dull coat",
        "cause": "Roundworms (Toxocara canis), hookworms (Ancylostoma), whipworms (Trichuris), tapeworms (Dipylidium, Taenia).",
        "prevention": "Regular deworming every 3–6 months. Flea control (tapeworm prevention). Good sanitation.",
        "treatment": "Fenbendazole for roundworms/hookworms/whipworms. Praziquantel for tapeworms.",
        "medicines": ["Fenbendazole 10% Suspension", "Praziquantel Tablet 50mg"],
    },
    {
        "name": "Bovine Respiratory Disease (BRD)",
        "animal": "Cattle",
        "symptoms": "Fever (above 40°C), rapid or labored breathing, nasal discharge, coughing, depression, loss of appetite, droopy ears",
        "cause": "Multifactorial: Mannheimia haemolytica, Pasteurella multocida, viral pathogens (BRSV, BHV-1). Triggered by stress, weaning, transport.",
        "prevention": "Vaccination. Minimize transport stress. Good nutrition. Adequate ventilation.",
        "treatment": "Oxytetracycline or Enrofloxacin. Anti-inflammatory (Dexamethasone). Vitamin B complex for recovery support.",
        "medicines": ["Dexamethasone 0.2% Injection", "Vitamin B-Complex Injection"],
    },
    {
        "name": "Cattle Roundworm Infestation",
        "animal": "Cattle",
        "symptoms": "Weight loss, rough coat, bottle jaw (edema under jaw), reduced milk production, diarrhea, anemia, weakness",
        "cause": "Haemonchus contortus (barber's pole worm), Ostertagia ostertagi, Cooperia species. Larvae ingested from pasture.",
        "prevention": "Strategic deworming. Pasture rotation. Avoid overgrazing.",
        "treatment": "Ivermectin injection. Follow up in 4 weeks if severe infestation.",
        "medicines": ["Ivermectin 1%"],
    },
    {
        "name": "Swine Respiratory Disease",
        "animal": "Pig",
        "symptoms": "Coughing, labored breathing, fever, nasal discharge, reduced growth rate, poor feed conversion, mortality in severe cases",
        "cause": "PRRS virus, Mycoplasma hyopneumoniae, Actinobacillus pleuropneumoniae. Often polymicrobial.",
        "prevention": "Vaccination (PRRS). Biosecurity. All-in/all-out management. Adequate ventilation.",
        "treatment": "Enrofloxacin for bacterial component. Wound/lesion care with Povidone Iodine.",
        "medicines": ["Enrofloxacin 10%", "Povidone Iodine 10% Solution"],
    },
    {
        "name": "Goat Gastrointestinal Parasitism",
        "animal": "Goat",
        "symptoms": "Weight loss, pale mucous membranes (anemia), bottle jaw, diarrhea, decreased milk production, lethargy, rough coat",
        "cause": "Haemonchus contortus (most common), liver fluke (Fasciola hepatica), other strongyle worms. Tropical climate increases risk.",
        "prevention": "FAMACHA scoring to identify anemic animals. Strategic deworming. Pasture management.",
        "treatment": "Albendazole (effective against both roundworms and liver fluke). Supportive nutrition.",
        "medicines": ["Albendazole 10%"],
    },
]


async def seed():
    """Main seeding function."""
    print("🌱 Starting database seed...")

    async with AsyncSessionLocal() as db:
        try:
            # ── Create tables if not exist ────────────────────────────────
            async with engine.begin() as conn:
                await conn.run_sync(Base.metadata.create_all)
            print("✅ Tables created/verified")

            # ── Animal Types ──────────────────────────────────────────────
            animal_map = {}
            for at_data in ANIMAL_TYPES:
                from sqlalchemy import select
                existing = (await db.execute(
                    select(AnimalType).where(AnimalType.name == at_data["name"])
                )).scalar_one_or_none()
                if not existing:
                    at = AnimalType(**at_data)
                    db.add(at)
                    await db.flush()
                    animal_map[at_data["name"]] = at
                    print(f"  ➕ Animal Type: {at_data['name']}")
                else:
                    animal_map[at_data["name"]] = existing
                    print(f"  ✓ Exists: {at_data['name']}")

            # ── Categories ────────────────────────────────────────────────
            category_map = {}
            for cat_data in CATEGORIES:
                from sqlalchemy import select
                existing = (await db.execute(
                    select(Category).where(Category.name == cat_data["name"])
                )).scalar_one_or_none()
                if not existing:
                    cat = Category(**cat_data)
                    db.add(cat)
                    await db.flush()
                    category_map[cat_data["name"]] = cat
                    print(f"  ➕ Category: {cat_data['name']}")
                else:
                    category_map[cat_data["name"]] = existing
                    print(f"  ✓ Exists: {cat_data['name']}")

            # ── Medicines ─────────────────────────────────────────────────
            medicine_map = {}
            for med_data in MEDICINES_DATA:
                from sqlalchemy import select
                existing = (await db.execute(
                    select(Medicine).where(Medicine.sku == med_data["sku"])
                )).scalar_one_or_none()
                if existing:
                    medicine_map[med_data["name"]] = existing
                    print(f"  ✓ Exists: {med_data['name']}")
                    continue

                animal_type = animal_map.get(med_data.pop("animal"))
                category = category_map.get(med_data.pop("category"))

                med = Medicine(
                    **med_data,
                    animal_type_id=animal_type.id if animal_type else None,
                    category_id=category.id if category else None,
                )
                db.add(med)
                await db.flush()
                medicine_map[med_data["name"]] = med
                print(f"  ➕ Medicine: {med_data['name']}")

            # ── Diseases ──────────────────────────────────────────────────
            for dis_data in DISEASES_DATA:
                from sqlalchemy import select
                existing = (await db.execute(
                    select(Disease).where(Disease.name == dis_data["name"])
                )).scalar_one_or_none()
                if existing:
                    print(f"  ✓ Exists: {dis_data['name']}")
                    continue

                animal_type = animal_map.get(dis_data.pop("animal"))
                medicine_names = dis_data.pop("medicines", [])

                disease = Disease(
                    **dis_data,
                    animal_type_id=animal_type.id if animal_type else None,
                )
                db.add(disease)
                await db.flush()

                # Link recommended medicines
                from app.models.models import disease_medicines
                from sqlalchemy import insert
                for med_name in medicine_names:
                    med = medicine_map.get(med_name)
                    if med:
                        await db.execute(insert(disease_medicines).values(disease_id=disease.id, medicine_id=med.id))

                print(f"  ➕ Disease: {dis_data['name']}")

            await db.commit()
            print("\n✅ Seed completed successfully!")
            print(f"   - {len(ANIMAL_TYPES)} animal types")
            print(f"   - {len(CATEGORIES)} categories")
            print(f"   - {len(MEDICINES_DATA)} medicines")
            print(f"   - {len(DISEASES_DATA)} diseases")

        except Exception as e:
            await db.rollback()
            print(f"\n❌ Seed failed: {e}")
            raise


if __name__ == "__main__":
    asyncio.run(seed())
