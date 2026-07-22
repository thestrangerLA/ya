'use client';
import { use, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { Edit, Trash2, ArrowLeft, Package, Calendar, DollarSign } from 'lucide-react';
import Link from 'next/link';
import { useRouter } from 'next/navigation';
import { PageHeader } from '@/components/ui/PageHeader';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ConfirmModal } from '@/components/ui/ConfirmModal';
import { ImageGallery } from '@/components/ui/ImageGallery';
import { medicineApi } from '@/lib/api';
import { formatCurrency, getStockStatus, getExpiryStatus } from '@/lib/utils';

export default function MedicineDetailPage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const qc = useQueryClient();
  const [showDelete, setShowDelete] = useState(false);

  const { data: medicine, isLoading } = useQuery({
    queryKey: ['medicine', id],
    queryFn: () => medicineApi.get(id),
  });

  const deleteMutation = useMutation({
    mutationFn: () => medicineApi.delete(id),
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['medicines'] }); router.push('/medicines'); },
  });

  if (isLoading || deleteMutation.isSuccess) return <LoadingSpinner />;
  if (!medicine) return <div className="page-body"><div className="alert alert-danger">ไม่พบข้อมูลยาในระบบ</div></div>;

  const stock = getStockStatus(medicine.stock_quantity);
  const expiry = getExpiryStatus(medicine.expiration_date);

  return (
    <div>
      <PageHeader title={medicine.name} subtitle={medicine.brand ? `ยี่ห้อ: ${medicine.brand}` : undefined}>
        <Link href="/medicines" className="btn btn-secondary btn-sm"><ArrowLeft size={14} /> ย้อนกลับ</Link>
        <Link href={`/medicines/${id}/edit`} className="btn btn-secondary"><Edit size={15} /> แก้ไขข้อมูล</Link>
        <button className="btn btn-danger" onClick={() => setShowDelete(true)}><Trash2 size={15} /> ลบ</button>
      </PageHeader>

      <div className="page-body">
        <div style={{ display: 'grid', gridTemplateColumns: '320px 1fr', gap: 24, alignItems: 'start' }}>
          {/* Left: Image Gallery + Quick Stats */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            <ImageGallery images={medicine.images} />
            <div className="card">
              <div style={{ display: 'flex', flexDirection: 'column', gap: 12 }}>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: 13, color: '#6b7280', display: 'flex', alignItems: 'center', gap: 6 }}><Package size={14} /> คงเหลือ</span>
                  <span className={`badge ${stock.color.includes('green') ? 'badge-green' : stock.color.includes('amber') ? 'badge-amber' : 'badge-red'}`}>{medicine.stock_quantity} ชิ้น</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: 13, color: '#6b7280', display: 'flex', alignItems: 'center', gap: 6 }}><DollarSign size={14} /> ราคา</span>
                  <span style={{ fontWeight: 700, color: '#111827' }}>{formatCurrency(medicine.price)}</span>
                </div>
                <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                  <span style={{ fontSize: 13, color: '#6b7280', display: 'flex', alignItems: 'center', gap: 6 }}><Calendar size={14} /> วันหมดอายุ</span>
                  <span className={`badge ${expiry.color.includes('green') ? 'badge-green' : expiry.color.includes('amber') ? 'badge-amber' : 'badge-red'}`}>{expiry.label}</span>
                </div>
                {medicine.sku && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: 13, color: '#6b7280' }}>รหัส SKU</span>
                    <code style={{ fontSize: 12, background: '#f3f4f6', padding: '2px 6px', borderRadius: 4 }}>{medicine.sku}</code>
                  </div>
                )}
                {medicine.animal_type && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: 13, color: '#6b7280' }}>ประเภทสัตว์</span>
                    <span className="badge badge-blue">{medicine.animal_type.icon} {medicine.animal_type.name}</span>
                  </div>
                )}
                {medicine.category && (
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontSize: 13, color: '#6b7280' }}>หมวดหมู่</span>
                    <span className="badge badge-gray">{medicine.category.name}</span>
                  </div>
                )}
              </div>
            </div>
          </div>

          {/* Right: Details */}
          <div style={{ display: 'flex', flexDirection: 'column', gap: 16 }}>
            {/* Pregnancy Safety Card */}
            {medicine.notes && (() => {
              const notesLower = medicine.notes.toLowerCase();
              const isForbidden = notesLower.includes('ห้ามใช้') || notesLower.includes('เด็ดขาด') || notesLower.includes('teratogenic');
              const isCaution = notesLower.includes('หลีกเลี่ยง') || notesLower.includes('ระมัดระวัง') || notesLower.includes('ควรหลีกเลี่ยง');
              const isSafe = notesLower.includes('ปลอดภัยสูง') || notesLower.includes('ปลอดภัยมาก') || notesLower.includes('ปลอดภัยและมีประโยชน์');
              const bgColor = isForbidden ? '#fef2f2' : isCaution ? '#fffbeb' : isSafe ? '#f0fdf4' : '#f0f9ff';
              const borderColor = isForbidden ? '#fca5a5' : isCaution ? '#fcd34d' : isSafe ? '#86efac' : '#7dd3fc';
              const textColor = isForbidden ? '#b91c1c' : isCaution ? '#92400e' : isSafe ? '#15803d' : '#0369a1';
              const icon = isForbidden ? '🛑' : isCaution ? '⚠️' : isSafe ? '✅' : 'ℹ️';
              const title = isForbidden ? 'ห้ามใช้ในสัตว์ตั้งท้อง' : isCaution ? 'ใช้ด้วยความระมัดระวังในสัตว์ตั้งท้อง' : isSafe ? 'ปลอดภัยสำหรับสัตว์ตั้งท้อง' : 'ข้อมูลสำหรับสัตว์ตั้งท้อง';
              return (
                <div style={{ background: bgColor, border: `1.5px solid ${borderColor}`, borderRadius: 12, padding: '14px 18px' }}>
                  <div style={{ display: 'flex', alignItems: 'center', gap: 8, marginBottom: 8 }}>
                    <span style={{ fontSize: 18 }}>{icon}</span>
                    <h3 style={{ fontSize: 13, fontWeight: 700, color: textColor, margin: 0 }}>🤰 {title}</h3>
                  </div>
                  <p style={{ fontSize: 14, color: textColor, lineHeight: 1.7, margin: 0, whiteSpace: 'pre-wrap' }}>{medicine.notes}</p>
                </div>
              );
            })()}

            {[
              { label: '📋 รายละเอียดและคุณสมบัติ', value: medicine.description },
              { label: '✅ ข้อบ่งใช้ / สรรพคุณ (Indications)', value: medicine.indications },
              { label: '💉 ขนาดและปริมาณการใช้ (Dosage)', value: medicine.dosage },
              { label: '📌 วิธีการใช้ยา (Usage Instructions)', value: medicine.usage },
              { label: '⚠️ ข้อระวังและข้อห้ามใช้ (Warnings)', value: medicine.warnings },
              { label: '🔴 ผลข้างเคียงที่อาจเกิดขึ้น (Side Effects)', value: medicine.side_effects },
              { label: '📦 การเก็บรักษา (Storage)', value: medicine.storage },
            ].filter(f => f.value).map(f => (
              <div key={f.label} className="card">
                <h3 style={{ fontSize: 13, fontWeight: 700, marginBottom: 8, color: '#374151' }}>{f.label}</h3>
                <p style={{ fontSize: 14, color: '#374151', lineHeight: 1.7, whiteSpace: 'pre-wrap' }}>{f.value}</p>
              </div>
            ))}
          </div>
        </div>
      </div>

      <ConfirmModal
        isOpen={showDelete}
        title="ยืนยันการลบเวชภัณฑ์ยา"
        message={`คุณแน่ใจหรือไม่ว่าต้องการลบรายการ "${medicine.name}"?`}
        onConfirm={() => deleteMutation.mutate()}
        onCancel={() => setShowDelete(false)}
        loading={deleteMutation.isPending}
      />
    </div>
  );
}
