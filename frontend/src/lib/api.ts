/**
 * Axios-based API client for the Animal Medicine Information System.
 * All methods return typed responses matching backend schemas.
 */

import axios, { AxiosInstance, AxiosRequestConfig } from 'axios';
import type {
  AnimalType, AnimalTypeCreate, AnimalTypeUpdate,
  Category, CategoryCreate, CategoryUpdate,
  Medicine, MedicineListItem, MedicineCreate, MedicineUpdate, MedicineImage,
  Disease, DiseaseListItem, DiseaseCreate, DiseaseUpdate,
  DashboardStats, RecentMedicine,
  SearchResult, SearchType,
  AIResponse,
  InventoryReport,
  PaginatedResponse, MessageResponse,
  MedicineListParams, DiseaseListParams,
} from '@/types';

const API_BASE = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000';

const axiosInstance: AxiosInstance = axios.create({
  baseURL: `${API_BASE}/api/v1`,
  headers: { 'Content-Type': 'application/json' },
  timeout: 30000,
});

// ── Error handling interceptor ─────────────────────────────────────────────
axiosInstance.interceptors.response.use(
  (response) => response,
  (error) => {
    const message =
      error.response?.data?.detail ||
      error.response?.data?.message ||
      error.message ||
      'An unexpected error occurred';
    return Promise.reject(new Error(message));
  }
);

function buildParams(obj: Record<string, unknown>): URLSearchParams {
  const params = new URLSearchParams();
  Object.entries(obj).forEach(([k, v]) => {
    if (v !== undefined && v !== null && v !== '') {
      params.append(k, String(v));
    }
  });
  return params;
}

// ════════════════════════════════════════════════════════════════════════════
// Animal Types
// ════════════════════════════════════════════════════════════════════════════

export const animalTypeApi = {
  list: (page = 1, pageSize = 100) =>
    axiosInstance
      .get<PaginatedResponse<AnimalType>>('/animal-types/', {
        params: { page, page_size: pageSize },
      })
      .then((r) => r.data),

  get: (id: string) =>
    axiosInstance.get<AnimalType>(`/animal-types/${id}`).then((r) => r.data),

  create: (data: AnimalTypeCreate) =>
    axiosInstance.post<AnimalType>('/animal-types/', data).then((r) => r.data),

  update: (id: string, data: AnimalTypeUpdate) =>
    axiosInstance.patch<AnimalType>(`/animal-types/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    axiosInstance.delete<MessageResponse>(`/animal-types/${id}`).then((r) => r.data),
};

// ════════════════════════════════════════════════════════════════════════════
// Categories
// ════════════════════════════════════════════════════════════════════════════

export const categoryApi = {
  list: (page = 1, pageSize = 100) =>
    axiosInstance
      .get<PaginatedResponse<Category>>('/categories/', {
        params: { page, page_size: pageSize },
      })
      .then((r) => r.data),

  get: (id: string) =>
    axiosInstance.get<Category>(`/categories/${id}`).then((r) => r.data),

  create: (data: CategoryCreate) =>
    axiosInstance.post<Category>('/categories/', data).then((r) => r.data),

  update: (id: string, data: CategoryUpdate) =>
    axiosInstance.patch<Category>(`/categories/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    axiosInstance.delete<MessageResponse>(`/categories/${id}`).then((r) => r.data),
};

// ════════════════════════════════════════════════════════════════════════════
// Medicines
// ════════════════════════════════════════════════════════════════════════════

export const medicineApi = {
  list: (params: MedicineListParams = {}) =>
    axiosInstance
      .get<PaginatedResponse<MedicineListItem>>('/medicines/', { params })
      .then((r) => r.data),

  get: (id: string) =>
    axiosInstance.get<Medicine>(`/medicines/${id}`).then((r) => r.data),

  create: (data: MedicineCreate) =>
    axiosInstance.post<Medicine>('/medicines/', data).then((r) => r.data),

  update: (id: string, data: MedicineUpdate) =>
    axiosInstance.patch<Medicine>(`/medicines/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    axiosInstance.delete<MessageResponse>(`/medicines/${id}`).then((r) => r.data),

  // ── Images ──────────────────────────────────────────────────────────────

  uploadImage: (medicineId: string, file: File, isPrimary = false) => {
    const form = new FormData();
    form.append('file', file);
    return axiosInstance
      .post<MedicineImage>(`/medicines/${medicineId}/images?is_primary=${isPrimary}`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then((r) => r.data);
  },

  uploadImages: (medicineId: string, files: File[]) => {
    const form = new FormData();
    files.forEach((f) => form.append('files', f));
    return axiosInstance
      .post<MedicineImage[]>(`/medicines/${medicineId}/images/batch`, form, {
        headers: { 'Content-Type': 'multipart/form-data' },
      })
      .then((r) => r.data);
  },

  setPrimaryImage: (medicineId: string, imageId: string) =>
    axiosInstance
      .patch<MessageResponse>(`/medicines/${medicineId}/images/${imageId}/set-primary`)
      .then((r) => r.data),

  deleteImage: (medicineId: string, imageId: string) =>
    axiosInstance
      .delete<MessageResponse>(`/medicines/${medicineId}/images/${imageId}`)
      .then((r) => r.data),
};

// ════════════════════════════════════════════════════════════════════════════
// Diseases
// ════════════════════════════════════════════════════════════════════════════

export const diseaseApi = {
  list: (params: DiseaseListParams = {}) =>
    axiosInstance
      .get<PaginatedResponse<DiseaseListItem>>('/diseases/', { params })
      .then((r) => r.data),

  get: (id: string) =>
    axiosInstance.get<Disease>(`/diseases/${id}`).then((r) => r.data),

  create: (data: DiseaseCreate) =>
    axiosInstance.post<Disease>('/diseases/', data).then((r) => r.data),

  update: (id: string, data: DiseaseUpdate) =>
    axiosInstance.patch<Disease>(`/diseases/${id}`, data).then((r) => r.data),

  delete: (id: string) =>
    axiosInstance.delete<MessageResponse>(`/diseases/${id}`).then((r) => r.data),
};

// ════════════════════════════════════════════════════════════════════════════
// Dashboard
// ════════════════════════════════════════════════════════════════════════════

export const dashboardApi = {
  stats: () =>
    axiosInstance.get<DashboardStats>('/dashboard/stats').then((r) => r.data),

  recentMedicines: (limit = 5) =>
    axiosInstance
      .get<RecentMedicine[]>('/dashboard/recent-medicines', { params: { limit } })
      .then((r) => r.data),
};

// ════════════════════════════════════════════════════════════════════════════
// Search
// ════════════════════════════════════════════════════════════════════════════

export const searchApi = {
  search: (params: {
    query: string;
    animal_type_id?: string;
    category_id?: string;
    search_type?: SearchType;
    page?: number;
    page_size?: number;
  }) =>
    axiosInstance
      .get<SearchResult>('/search/', { params })
      .then((r) => r.data),
};

// ════════════════════════════════════════════════════════════════════════════
// AI Assistant
// ════════════════════════════════════════════════════════════════════════════

export const aiApi = {
  query: (query: string, animalTypeId?: string) =>
    axiosInstance
      .post<AIResponse>('/ai/query', {
        query,
        animal_type_id: animalTypeId,
      })
      .then((r) => r.data),
};

// ════════════════════════════════════════════════════════════════════════════
// Inventory
// ════════════════════════════════════════════════════════════════════════════

export const inventoryApi = {
  report: () =>
    axiosInstance.get<InventoryReport>('/inventory/report').then((r) => r.data),
};

// ════════════════════════════════════════════════════════════════════════════
// AI Marketing
// ════════════════════════════════════════════════════════════════════════════

export const marketingApi = {
  copy: (medicineId: string, tone = 'Professional', targetAudience = 'เกษตรกรและคนเลี้ยงสัตว์') =>
    axiosInstance.post('/marketing/copy', { medicine_id: medicineId, tone, target_audience: targetAudience }).then((r) => r.data),

  campaign: (medicineId: string, campaignType = 'Flash Sale') =>
    axiosInstance.post('/marketing/campaign', { medicine_id: medicineId, campaign_type: campaignType }).then((r) => r.data),

  imagePrompt: (medicineId: string, colorTheme = 'Green & Gold', marketingGoal = 'Premium Advertising Poster') =>
    axiosInstance.post('/marketing/image-prompt', { medicine_id: medicineId, color_theme: colorTheme, marketing_goal: marketingGoal }).then((r) => r.data),

  socialContent: (medicineId: string) =>
    axiosInstance.post('/marketing/social-content', { medicine_id: medicineId }).then((r) => r.data),

  ideas: () =>
    axiosInstance.post('/marketing/ideas').then((r) => r.data),

  seo: (medicineId: string) =>
    axiosInstance.post('/marketing/seo', { medicine_id: medicineId }).then((r) => r.data),

  calendar: (medicineId: string) =>
    axiosInstance.post('/marketing/calendar', { medicine_id: medicineId }).then((r) => r.data),

  oneClick: (medicineId: string) =>
    axiosInstance.post('/marketing/one-click', { medicine_id: medicineId }).then((r) => r.data),
};

export default axiosInstance;
