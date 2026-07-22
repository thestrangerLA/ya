'use client';

import { useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Plus, Search, Edit, Trash2, Eye, ChevronUp, ChevronDown } from 'lucide-react';
import Link from 'next/link';
import { PageHeader } from '@/components/ui/PageHeader';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ConfirmModal } from '@/components/ui/ConfirmModal';
import { medicineApi, animalTypeApi, categoryApi } from '@/lib/api';
import { formatDate, formatCurrency, getStockStatus, getExpiryStatus } from '@/lib/utils';

export default function MedicinesPage() {
  const qc = useQueryClient();
  const [page, setPage] = useState(1);
  const [search, setSearch] = useState('');
  const [animalTypeId, setAnimalTypeId] = useState('');
  const [categoryId, setCategoryId] = useState('');
  const [sortBy, setSortBy] = useState('created_at');
  const [sortOrder, setSortOrder] = useState<'asc'|'desc'>('desc');
  const [deleteId, setDeleteId] = useState<string | null>(null);
  const [deleteName, setDeleteName] = useState('');

  const { data, isLoading } = useQuery({
    queryKey: ['medicines', page, search, animalTypeId, categoryId, sortBy, sortOrder],
    queryFn: () => medicineApi.list({
      page,
      page_size: 20,
      search: search || undefined,
      animal_type_id: animalTypeId || undefined,
      category_id: categoryId || undefined,
      sort_by: sortBy,
      sort_order: sortOrder
    }),
  });

  const { data: animalTypes } = useQuery({ queryKey: ['animal-types'], queryFn: () => animalTypeApi.list() });
  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: () => categoryApi.list() });

  const deleteMutation = useMutation({
    mutationFn: (id: string) => medicineApi.delete(id),
    onSuccess: () => {
      qc.invalidateQueries({ queryKey: ['medicines'] });
      qc.invalidateQueries({ queryKey: ['dashboard-stats'] });
      setDeleteId(null);
    },
  });

  function toggleSort(col: string) {
    if (sortBy === col) setSortOrder(o => o === 'asc' ? 'desc' : 'asc');
    else { setSortBy(col); setSortOrder('desc'); }
    setPage(1);
  }

  function SortIcon({ col }: { col: string }) {
    if (sortBy !== col) return null;
    return sortOrder === 'asc' ? <ChevronUp size={12} /> : <ChevronDown size={12} />;
  }

  return (
    <div>
      <PageHeader title="คลังเวชภัณฑ์ยา" subtitle={`รวมทั้งหมด ${data?.meta?.total ?? '—'} รายการ`}>
        <Link href="/medicines/new" className="btn btn-primary"><Plus size={16} /> เพิ่มเวชภัณฑ์ยา</Link>
      </PageHeader>

      <div className="page-body">
        {/* Filters */}
        <div className="card" style={{ marginBottom: 20 }}>
          <div style={{ display: 'flex', gap: 10, flexWrap: 'wrap', alignItems: 'flex-end' }}>
            <div className="search-bar" style={{ flex: 1, minWidth: 200 }}>
              <Search className="search-bar-icon" />
              <input
                className="form-input"
                placeholder="ค้นหาชื่อยา, ยี่ห้อ, SKU..."
                value={search}
                onChange={e => { setSearch(e.target.value); setPage(1); }}
                style={{ paddingLeft: 38 }}
              />
            </div>
            <div style={{ minWidth: 160 }}>
              <select className="form-select" value={animalTypeId} onChange={e => { setAnimalTypeId(e.target.value); setPage(1); }}>
                <option value="">สัตว์ทุกประเภท</option>
                {animalTypes?.data.map(at => <option key={at.id} value={at.id}>{at.icon} {at.name}</option>)}
              </select>
            </div>
            <div style={{ minWidth: 160 }}>
              <select className="form-select" value={categoryId} onChange={e => { setCategoryId(e.target.value); setPage(1); }}>
                <option value="">ทุกหมวดหมู่ยา</option>
                {categories?.data.map(cat => <option key={cat.id} value={cat.id}>{cat.name}</option>)}
              </select>
            </div>
            {(search || animalTypeId || categoryId) && (
              <button className="btn btn-ghost btn-sm" onClick={() => { setSearch(''); setAnimalTypeId(''); setCategoryId(''); setPage(1); }}>ล้างตัวกรอง</button>
            )}
          </div>
        </div>

        {/* Table */}
        <div className="table-container">
          {isLoading ? <LoadingSpinner /> : (
            <table className="table">
              <thead>
                <tr>
                  <th>รูป</th>
                  <th style={{ cursor: 'pointer' }} onClick={() => toggleSort('name')}>ชื่อเวชภัณฑ์ยา <SortIcon col="name" /></th>
                  <th>ประเภทสัตว์</th>
                  <th>หมวดหมู่</th>
                  <th style={{ cursor: 'pointer' }} onClick={() => toggleSort('stock_quantity')}>จำนวนคงเหลือ <SortIcon col="stock_quantity" /></th>
                  <th style={{ cursor: 'pointer' }} onClick={() => toggleSort('expiration_date')}>วันหมดอายุ <SortIcon col="expiration_date" /></th>
                  <th style={{ cursor: 'pointer' }} onClick={() => toggleSort('price')}>ราคา <SortIcon col="price" /></th>
                  <th>จัดการ</th>
                </tr>
              </thead>
              <tbody>
                {data?.data?.map(med => {
                  const stock = getStockStatus(med.stock_quantity);
                  const expiry = getExpiryStatus(med.expiration_date);
                  return (
                    <tr key={med.id}>
                      <td>
                        <div style={{ width: 40, height: 40, borderRadius: 8, overflow: 'hidden', background: '#f9fafb', border: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'center' }}>
                          {med.primary_image_url ? <img src={med.primary_image_url} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} /> : <span style={{ fontSize: 18 }}>💊</span>}
                        </div>
                      </td>
                      <td>
                        <div style={{ fontWeight: 600 }}>{med.name}</div>
                        {med.brand && <div style={{ fontSize: 12, color: '#6b7280' }}>ยี่ห้อ: {med.brand}</div>}
                        {med.sku && <div style={{ fontSize: 11, color: '#9ca3af' }}>SKU: #{med.sku}</div>}
                      </td>
                      <td>{med.animal_type ? <span className="badge badge-blue">{med.animal_type.icon} {med.animal_type.name}</span> : '—'}</td>
                      <td>{med.category ? <span className="badge badge-gray">{med.category.name}</span> : '—'}</td>
                      <td><span className={`badge ${stock.color.includes('green') ? 'badge-green' : stock.color.includes('amber') ? 'badge-amber' : 'badge-red'}`}>{med.stock_quantity}</span></td>
                      <td><span className={`badge ${expiry.color.includes('green') ? 'badge-green' : expiry.color.includes('amber') ? 'badge-amber' : 'badge-red'}`}>{expiry.label}</span></td>
                      <td style={{ fontWeight: 500 }}>{formatCurrency(med.price)}</td>
                      <td>
                        <div style={{ display: 'flex', gap: 4 }}>
                          <Link href={`/medicines/${med.id}`} className="btn btn-ghost btn-icon btn-sm" title="ดูรายละเอียด"><Eye size={15} /></Link>
                          <Link href={`/medicines/${med.id}/edit`} className="btn btn-ghost btn-icon btn-sm" title="แก้ไข"><Edit size={15} /></Link>
                          <button className="btn btn-danger btn-icon btn-sm" title="ลบ" onClick={() => { setDeleteId(med.id); setDeleteName(med.name); }}><Trash2 size={15} /></button>
                        </div>
                      </td>
                    </tr>
                  );
                })}
              </tbody>
            </table>
          )}

          {data && (
            <div className="pagination">
              <span>แสดง {((page-1)*20)+1}–{Math.min(page*20, data.meta.total)} จาก {data.meta.total} รายการ</span>
              <div className="pagination-controls">
                <button className="pagination-btn" disabled={page === 1} onClick={() => setPage(p => p-1)}>←</button>
                {Array.from({ length: Math.min(5, data.meta.total_pages) }, (_, i) => {
                  const p = Math.max(1, page - 2) + i;
                  if (p > data.meta.total_pages) return null;
                  return <button key={p} className={`pagination-btn${p === page ? ' active' : ''}`} onClick={() => setPage(p)}>{p}</button>;
                })}
                <button className="pagination-btn" disabled={page >= data.meta.total_pages} onClick={() => setPage(p => p+1)}>→</button>
              </div>
            </div>
          )}

          {!isLoading && data?.data?.length === 0 && (
            <div className="empty-state">
              <div style={{ fontSize: 48, marginBottom: 16 }}>💊</div>
              <h3>ไม่พบข้อมูลเวชภัณฑ์ยา</h3>
              <p>ลองเปลี่ยนคำค้นหา หรือ <Link href="/medicines/new" style={{ color: '#16a34a' }}>คลิกเพื่อเพิ่มยาใหม่</Link></p>
            </div>
          )}
        </div>
      </div>

      <ConfirmModal
        isOpen={!!deleteId}
        title="ยืนยันการลบเวชภัณฑ์ยา"
        message={`คุณแน่ใจหรือไม่ว่าต้องการลบรายการ "${deleteName}"? การดำเนินการนี้ไม่สามารถยกเลิกได้`}
        onConfirm={() => deleteId && deleteMutation.mutate(deleteId)}
        onCancel={() => setDeleteId(null)}
        loading={deleteMutation.isPending}
      />
    </div>
  );
}
