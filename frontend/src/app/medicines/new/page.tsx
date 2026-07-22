'use client';
import { useState } from 'react';
import { useRouter } from 'next/navigation';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Save, ArrowLeft } from 'lucide-react';
import Link from 'next/link';
import { PageHeader } from '@/components/ui/PageHeader';
import { ImageUpload } from '@/components/ui/ImageUpload';
import { medicineApi, animalTypeApi, categoryApi } from '@/lib/api';
import type { MedicineCreate } from '@/types';

export default function NewMedicinePage() {
  const router = useRouter();
  const qc = useQueryClient();
  const [files, setFiles] = useState<File[]>([]);
  const [error, setError] = useState('');

  const [form, setForm] = useState<MedicineCreate>({
    name: '', brand: '', sku: '', stock_quantity: 0, price: undefined,
    animal_type_id: '', category_id: '', description: '', indications: '',
    dosage: '', usage: '', warnings: '', side_effects: '', storage: '', notes: '',
    expiration_date: '',
  });

  const { data: animalTypes } = useQuery({ queryKey: ['animal-types'], queryFn: () => animalTypeApi.list() });
  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: () => categoryApi.list() });

  const createMutation = useMutation({
    mutationFn: async (data: MedicineCreate) => {
      const med = await medicineApi.create(data);
      if (files.length > 0) {
        await medicineApi.uploadImages(med.id, files);
      }
      return med;
    },
    onSuccess: (med) => {
      qc.invalidateQueries({ queryKey: ['medicines'] });
      qc.invalidateQueries({ queryKey: ['dashboard-stats'] });
      router.push(`/medicines/${med.id}`);
    },
    onError: (e: Error) => setError(e.message),
  });

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');
    const cleaned: MedicineCreate = {
      ...form,
      animal_type_id: form.animal_type_id || undefined,
      category_id: form.category_id || undefined,
      expiration_date: form.expiration_date || undefined,
      brand: form.brand || undefined,
      sku: form.sku || undefined,
      price: form.price ? Number(form.price) : undefined,
    };
    createMutation.mutate(cleaned);
  }

  function field(key: keyof MedicineCreate) {
    return {
      value: (form[key] as string) ?? '',
      onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
        setForm(f => ({ ...f, [key]: e.target.value })),
    };
  }

  return (
    <div>
      <PageHeader title="เพิ่มเวชภัณฑ์ยาใหม่" subtitle="กรอกข้อมูลเวชภัณฑ์ยาและอัปโหลดรูปภาพ">
        <Link href="/medicines" className="btn btn-secondary btn-sm"><ArrowLeft size={14} /> ย้อนกลับ</Link>
      </PageHeader>

      <div className="page-body">
        {error && <div className="alert alert-danger" style={{ marginBottom: 16 }}>{error}</div>}

        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, alignItems: 'start' }}>
            {/* Left Column */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <div className="card">
                <h3 className="card-title" style={{ marginBottom: 16 }}>ข้อมูลพื้นฐาน</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                  <div className="form-group">
                    <label className="form-label">ชื่อเวชภัณฑ์ยา *</label>
                    <input className="form-input" placeholder="เช่น Oxytetracycline 20%" required {...field('name')} />
                  </div>
                  <div className="form-grid">
                    <div className="form-group">
                      <label className="form-label">ยี่ห้อ/แบรนด์ <span className="form-label-optional">(ถ้ามี)</span></label>
                      <input className="form-input" placeholder="ระบุยี่ห้อ" {...field('brand')} />
                    </div>
                    <div className="form-group">
                      <label className="form-label">รหัส SKU <span className="form-label-optional">(ถ้ามี)</span></label>
                      <input className="form-input" placeholder="เช่น MED-001" {...field('sku')} />
                    </div>
                  </div>
                  <div className="form-grid">
                    <div className="form-group">
                      <label className="form-label">ประเภทสัตว์</label>
                      <select className="form-select" {...field('animal_type_id')}>
                        <option value="">เลือกประเภทสัตว์...</option>
                        {animalTypes?.data.map(at => <option key={at.id} value={at.id}>{at.icon} {at.name}</option>)}
                      </select>
                    </div>
                    <div className="form-group">
                      <label className="form-label">หมวดหมู่ยา</label>
                      <select className="form-select" {...field('category_id')}>
                        <option value="">เลือกหมวดหมู่ยา...</option>
                        {categories?.data.map(cat => <option key={cat.id} value={cat.id}>{cat.name}</option>)}
                      </select>
                    </div>
                  </div>
                  <div className="form-grid">
                    <div className="form-group">
                      <label className="form-label">จำนวนสต็อกคงเหลือ *</label>
                      <input className="form-input" type="number" min="0" required {...field('stock_quantity')} />
                    </div>
                    <div className="form-group">
                      <label className="form-label">ราคา (บาท) <span className="form-label-optional">(ถ้ามี)</span></label>
                      <input className="form-input" type="number" min="0" step="0.01" placeholder="0.00" {...field('price')} />
                    </div>
                  </div>
                  <div className="form-group">
                    <label className="form-label">วันหมดอายุ <span className="form-label-optional">(ถ้ามี)</span></label>
                    <input className="form-input" type="date" {...field('expiration_date')} />
                  </div>
                </div>
              </div>

              <div className="card">
                <h3 className="card-title" style={{ marginBottom: 16 }}>รูปภาพสินค้า</h3>
                <ImageUpload onFilesChange={setFiles} maxFiles={10} />
              </div>
            </div>

            {/* Right Column */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <div className="card">
                <h3 className="card-title" style={{ marginBottom: 16 }}>ข้อมูลทางการแพทย์</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                  {[
                    { key: 'description', label: 'รายละเอียดและคุณสมบัติ', rows: 3 },
                    { key: 'indications', label: 'ข้อบ่งใช้ / สรรพคุณ (Indications)', rows: 3 },
                    { key: 'dosage', label: 'ขนาดและปริมาณการใช้ (Dosage)', rows: 3 },
                    { key: 'usage', label: 'วิธีใช้ (Usage Instructions)', rows: 3 },
                    { key: 'warnings', label: 'ข้อระวัง / ระยะหยุดยา (Warnings)', rows: 2 },
                    { key: 'side_effects', label: 'ผลข้างเคียง (Side Effects)', rows: 2 },
                    { key: 'storage', label: 'การเก็บรักษา (Storage)', rows: 2 },
                    { key: 'notes', label: 'หมายเหตุเพิ่มเติม (Notes)', rows: 2 }
                  ].map(({ key, label, rows }) => (
                    <div key={key} className="form-group">
                      <label className="form-label">{label} <span className="form-label-optional">(ถ้ามี)</span></label>
                      <textarea className="form-textarea" rows={rows} placeholder={`ระบุ ${label.toLowerCase()}...`} {...field(key as keyof MedicineCreate)} />
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
                <Link href="/medicines" className="btn btn-secondary">ยกเลิก</Link>
                <button type="submit" className="btn btn-primary btn-lg" disabled={createMutation.isPending}>
                  <Save size={16} />
                  {createMutation.isPending ? 'กำลังบันทึก...' : 'บันทึกข้อมูลยา'}
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
