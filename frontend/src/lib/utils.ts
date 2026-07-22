/**
 * Utility functions for the Animal Medicine Information System (Thai Edition).
 */

import { clsx, type ClassValue } from 'clsx';
import { twMerge } from 'tailwind-merge';
import { format, differenceInDays, parseISO } from 'date-fns';
import { th } from 'date-fns/locale';

/** Merge Tailwind class names intelligently */
export function cn(...inputs: ClassValue[]): string {
  return twMerge(clsx(inputs));
}

/** Format ISO date string to readable Thai date */
export function formatDate(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  try {
    return format(parseISO(dateStr), 'd MMM yyyy', { locale: th });
  } catch {
    return dateStr;
  }
}

/** Format ISO datetime string */
export function formatDateTime(dateStr: string | null | undefined): string {
  if (!dateStr) return '—';
  try {
    return format(parseISO(dateStr), 'd MMM yyyy HH:mm', { locale: th });
  } catch {
    return dateStr;
  }
}

/** Days remaining until a date */
export function daysUntil(dateStr: string | null | undefined): number | null {
  if (!dateStr) return null;
  try {
    return differenceInDays(parseISO(dateStr), new Date());
  } catch {
    return null;
  }
}

/** Format currency in Thai Baht (฿) */
export function formatCurrency(value: number | null | undefined): string {
  if (value === null || value === undefined) return '—';
  return new Intl.NumberFormat('th-TH', {
    style: 'currency',
    currency: 'THB',
    minimumFractionDigits: 2,
  }).format(value);
}

/** Format numbers with commas */
export function formatNumber(value: number): string {
  return new Intl.NumberFormat('th-TH').format(value);
}

/** Truncate text */
export function truncate(str: string | null | undefined, n: number): string {
  if (!str) return '';
  return str.length > n ? str.slice(0, n) + '…' : str;
}

/** Get expiry status label in Thai */
export function getExpiryStatus(dateStr: string | null | undefined): {
  label: string;
  color: string;
  bgColor: string;
} {
  if (!dateStr) return { label: 'ไม่ระบุวัน', color: 'text-gray-500', bgColor: 'bg-gray-100' };
  const days = daysUntil(dateStr);
  if (days === null) return { label: 'ไม่ระบุวัน', color: 'text-gray-500', bgColor: 'bg-gray-100' };
  if (days < 0) return { label: 'หมดอายุแล้ว', color: 'text-red-700', bgColor: 'bg-red-100' };
  if (days <= 7) return { label: `เหลือ ${days} วัน`, color: 'text-red-600', bgColor: 'bg-red-50' };
  if (days <= 30) return { label: `เหลือ ${days} วัน`, color: 'text-amber-600', bgColor: 'bg-amber-50' };
  return { label: formatDate(dateStr), color: 'text-green-700', bgColor: 'bg-green-50' };
}

/** Get stock status in Thai */
export function getStockStatus(qty: number, threshold = 10): {
  label: string;
  color: string;
  bgColor: string;
} {
  if (qty === 0) return { label: 'สินค้าหมด', color: 'text-red-700', bgColor: 'bg-red-100' };
  if (qty <= threshold) return { label: 'สต็อกต่ำ', color: 'text-amber-700', bgColor: 'bg-amber-100' };
  return { label: 'มีสินค้า', color: 'text-green-700', bgColor: 'bg-green-100' };
}

/** Build image URL */
export function getImageUrl(url: string | null | undefined): string {
  if (!url) return '/placeholder-medicine.png';
  return url;
}
