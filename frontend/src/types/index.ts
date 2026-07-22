/**
 * TypeScript interfaces for the Animal Medicine Information System.
 * Mirrors the backend Pydantic schemas exactly.
 */

// ── Pagination ────────────────────────────────────────────────────────────

export interface PaginationMeta {
  total: number;
  page: number;
  page_size: number;
  total_pages: number;
}

export interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

export interface MessageResponse {
  message: string;
  success: boolean;
}

// ── Animal Types ──────────────────────────────────────────────────────────

export interface AnimalType {
  id: string;
  name: string;
  description: string | null;
  icon: string | null;
  created_at: string;
  updated_at: string;
  medicine_count?: number;
  disease_count?: number;
}

export interface AnimalTypeCreate {
  name: string;
  description?: string;
  icon?: string;
}

export interface AnimalTypeUpdate {
  name?: string;
  description?: string;
  icon?: string;
}

// ── Categories ────────────────────────────────────────────────────────────

export interface Category {
  id: string;
  name: string;
  description: string | null;
  created_at: string;
  updated_at: string;
  medicine_count?: number;
}

export interface CategoryCreate {
  name: string;
  description?: string;
}

export interface CategoryUpdate {
  name?: string;
  description?: string;
}

// ── Medicine Images ───────────────────────────────────────────────────────

export interface MedicineImage {
  id: string;
  medicine_id: string;
  file_path: string;
  original_filename: string | null;
  file_size: number | null;
  mime_type: string | null;
  is_primary: boolean;
  sort_order: number;
  created_at: string;
  url: string | null;
}

// ── Medicines ─────────────────────────────────────────────────────────────

export interface Medicine {
  id: string;
  name: string;
  brand: string | null;
  sku: string | null;
  animal_type_id: string | null;
  category_id: string | null;
  description: string | null;
  indications: string | null;
  dosage: string | null;
  usage: string | null;
  warnings: string | null;
  side_effects: string | null;
  storage: string | null;
  notes: string | null;
  expiration_date: string | null;
  stock_quantity: number;
  price: number | null;
  created_at: string;
  updated_at: string;
  animal_type: AnimalType | null;
  category: Category | null;
  images: MedicineImage[];
}

export interface MedicineListItem {
  id: string;
  name: string;
  brand: string | null;
  sku: string | null;
  indications?: string | null;
  stock_quantity: number;
  price: number | null;
  expiration_date: string | null;
  created_at: string;
  animal_type: AnimalType | null;
  category: Category | null;
  primary_image_url: string | null;
}

export interface MedicineCreate {
  name: string;
  brand?: string;
  sku?: string;
  animal_type_id?: string;
  category_id?: string;
  description?: string;
  indications?: string;
  dosage?: string;
  usage?: string;
  warnings?: string;
  side_effects?: string;
  storage?: string;
  notes?: string;
  expiration_date?: string;
  stock_quantity: number;
  price?: number;
}

export type MedicineUpdate = Partial<MedicineCreate>;

// ── Diseases ──────────────────────────────────────────────────────────────

export interface Disease {
  id: string;
  name: string;
  animal_type_id: string | null;
  symptoms: string | null;
  cause: string | null;
  prevention: string | null;
  treatment: string | null;
  created_at: string;
  updated_at: string;
  animal_type: AnimalType | null;
  recommended_medicines: MedicineListItem[];
}

export interface DiseaseListItem {
  id: string;
  name: string;
  symptoms: string | null;
  created_at: string;
  animal_type: AnimalType | null;
  medicine_count?: number;
}

export interface DiseaseCreate {
  name: string;
  animal_type_id?: string;
  symptoms?: string;
  cause?: string;
  prevention?: string;
  treatment?: string;
  recommended_medicine_ids?: string[];
}

export interface DiseaseUpdate {
  name?: string;
  animal_type_id?: string;
  symptoms?: string;
  cause?: string;
  prevention?: string;
  treatment?: string;
  recommended_medicine_ids?: string[];
}

// ── Dashboard ─────────────────────────────────────────────────────────────

export interface DashboardStats {
  total_medicines: number;
  total_diseases: number;
  total_animal_types: number;
  low_stock_count: number;
  expiring_soon_count: number;
}

export interface RecentMedicine {
  id: string;
  name: string;
  brand: string | null;
  stock_quantity: number;
  created_at: string;
  primary_image_url: string | null;
  animal_type_name: string | null;
}

// ── Search ────────────────────────────────────────────────────────────────

export interface SearchResult {
  medicines: MedicineListItem[];
  diseases: DiseaseListItem[];
  total_medicines: number;
  total_diseases: number;
  query: string;
}

export type SearchType = 'all' | 'medicine' | 'disease';

// ── AI Assistant ──────────────────────────────────────────────────────────

export interface AIRecommendedMedicine {
  id: string;
  name: string;
  brand: string | null;
  dosage: string | null;
  warnings: string | null;
  stock_quantity: number;
  primary_image_url: string | null;
}

export interface AIMatchedDisease {
  id: string;
  name: string;
  symptoms: string | null;
  treatment: string | null;
  animal_type_name: string | null;
  recommended_medicines: AIRecommendedMedicine[];
  match_score: number;
  matched_keywords: string[];
}

export interface AIResponse {
  query: string;
  interpretation: string;
  possible_diseases: AIMatchedDisease[];
  all_recommended_medicines: AIRecommendedMedicine[];
  disclaimer: string;
}

// ── Inventory ─────────────────────────────────────────────────────────────

export interface LowStockItem {
  id: string;
  name: string;
  brand: string | null;
  stock_quantity: number;
  primary_image_url: string | null;
  animal_type_name: string | null;
}

export interface ExpiringItem {
  id: string;
  name: string;
  brand: string | null;
  expiration_date: string;
  stock_quantity: number;
  days_until_expiry: number;
  primary_image_url: string | null;
}

export interface InventoryReport {
  low_stock_items: LowStockItem[];
  expiring_items: ExpiringItem[];
  total_low_stock: number;
  total_expiring: number;
  total_stock_value: number | null;
}

// ── Query Params ──────────────────────────────────────────────────────────

export interface MedicineListParams {
  page?: number;
  page_size?: number;
  search?: string;
  animal_type_id?: string;
  category_id?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
  low_stock_only?: boolean;
  expiring_only?: boolean;
}

export interface DiseaseListParams {
  page?: number;
  page_size?: number;
  search?: string;
  animal_type_id?: string;
  sort_by?: string;
  sort_order?: 'asc' | 'desc';
}
