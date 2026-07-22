'use client';
import { use, useEffect, useState } from 'react';
import { useRouter } from 'next/navigation';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Save, ArrowLeft, Trash2 } from 'lucide-react';
import Link from 'next/link';
import { PageHeader } from '@/components/ui/PageHeader';
import { LoadingSpinner } from '@/components/ui/LoadingSpinner';
import { ImageUpload } from '@/components/ui/ImageUpload';
import { medicineApi, animalTypeApi, categoryApi } from '@/lib/api';
import type { MedicineUpdate } from '@/types';

export default function EditMedicinePage({ params }: { params: Promise<{ id: string }> }) {
  const { id } = use(params);
  const router = useRouter();
  const qc = useQueryClient();
  const [files, setFiles] = useState<File[]>([]);
  const [error, setError] = useState('');
  const [form, setForm] = useState<MedicineUpdate>({});

  const { data: medicine, isLoading } = useQuery({
    queryKey: ['medicine', id],
    queryFn: () => medicineApi.get(id),
  });

  const { data: animalTypes } = useQuery({ queryKey: ['animal-types'], queryFn: () => animalTypeApi.list() });
  const { data: categories } = useQuery({ queryKey: ['categories'], queryFn: () => categoryApi.list() });

  useEffect(() => {
    if (medicine) {
      setForm({
        name: medicine.name,
        brand: medicine.brand ?? '',
        sku: medicine.sku ?? '',
        animal_type_id: medicine.animal_type_id ?? '',
        category_id: medicine.category_id ?? '',
        description: medicine.description ?? '',
        indications: medicine.indications ?? '',
        dosage: medicine.dosage ?? '',
        usage: medicine.usage ?? '',
        warnings: medicine.warnings ?? '',
        side_effects: medicine.side_effects ?? '',
        storage: medicine.storage ?? '',
        notes: medicine.notes ?? '',
        stock_quantity: medicine.stock_quantity,
        price: medicine.price ?? undefined,
        expiration_date: medicine.expiration_date ?? '',
      });
    }
  }, [medicine]);

  const updateMutation = useMutation({
    mutationFn: async (data: MedicineUpdate) => {
      const updated = await medicineApi.update(id, data);
      if (files.length > 0) await medicineApi.uploadImages(id, files);
      return updated;
    },
    onSuccess: () => { qc.invalidateQueries({ queryKey: ['medicine', id] }); qc.invalidateQueries({ queryKey: ['medicines'] }); router.push(`/medicines/${id}`); },
    onError: (e: Error) => setError(e.message),
  });

  const deleteImageMutation = useMutation({
    mutationFn: (imageId: string) => medicineApi.deleteImage(id, imageId),
    onSuccess: () => qc.invalidateQueries({ queryKey: ['medicine', id] }),
  });

  if (isLoading) return <LoadingSpinner />;
  if (!medicine) return <div className="page-body"><div className="alert alert-danger">Medicine not found.</div></div>;

  function handleSubmit(e: React.FormEvent) {
    e.preventDefault();
    setError('');
    const cleaned = { ...form, animal_type_id: (form.animal_type_id as string) || undefined, category_id: (form.category_id as string) || undefined, expiration_date: (form.expiration_date as string) || undefined, brand: (form.brand as string) || undefined, sku: (form.sku as string) || undefined };
    updateMutation.mutate(cleaned);
  }

  function field(key: keyof MedicineUpdate) {
    return {
      value: (form[key] as string) ?? '',
      onChange: (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) =>
        setForm(f => ({ ...f, [key]: e.target.value })),
    };
  }

  return (
    <div>
      <PageHeader title={`Edit: ${medicine.name}`} subtitle="Update medicine information">
        <Link href={`/medicines/${id}`} className="btn btn-secondary btn-sm"><ArrowLeft size={14} /> Back</Link>
      </PageHeader>
      <div className="page-body">
        {error && <div className="alert alert-danger" style={{ marginBottom: 16 }}>{error}</div>}
        <form onSubmit={handleSubmit}>
          <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: 24, alignItems: 'start' }}>
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <div className="card">
                <h3 className="card-title" style={{ marginBottom: 16 }}>Basic Information</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                  <div className="form-group">
                    <label className="form-label">Medicine Name *</label>
                    <input className="form-input" required {...field('name')} />
                  </div>
                  <div className="form-grid">
                    <div className="form-group"><label className="form-label">Brand</label><input className="form-input" {...field('brand')} /></div>
                    <div className="form-group"><label className="form-label">SKU</label><input className="form-input" {...field('sku')} /></div>
                  </div>
                  <div className="form-grid">
                    <div className="form-group">
                      <label className="form-label">Animal Type</label>
                      <select className="form-select" {...field('animal_type_id')}>
                        <option value="">Select animal...</option>
                        {animalTypes?.data.map(at => <option key={at.id} value={at.id}>{at.icon} {at.name}</option>)}
                      </select>
                    </div>
                    <div className="form-group">
                      <label className="form-label">Category</label>
                      <select className="form-select" {...field('category_id')}>
                        <option value="">Select category...</option>
                        {categories?.data.map(cat => <option key={cat.id} value={cat.id}>{cat.name}</option>)}
                      </select>
                    </div>
                  </div>
                  <div className="form-grid">
                    <div className="form-group">
                      <label className="form-label">Stock Quantity *</label>
                      <input className="form-input" type="number" min="0" required {...field('stock_quantity')} />
                    </div>
                    <div className="form-group">
                      <label className="form-label">Price <span className="form-label-optional">(optional)</span></label>
                      <input className="form-input" type="number" min="0" step="0.01" placeholder="0.00" {...field('price')} />
                    </div>
                  </div>
                  <div className="form-group">
                    <label className="form-label">Expiration Date <span className="form-label-optional">(optional)</span></label>
                    <input className="form-input" type="date" {...field('expiration_date')} />
                  </div>
                </div>
              </div>

              <div className="card">
                <h3 className="card-title" style={{ marginBottom: 16 }}>Product Images</h3>
                <ImageUpload 
                  onFilesChange={setFiles} 
                  maxFiles={10} 
                  existingImages={medicine.images} 
                  onDeleteExisting={(imgId) => deleteImageMutation.mutate(imgId)} 
                />
              </div>
            </div>

            {/* Right Column */}
            <div style={{ display: 'flex', flexDirection: 'column', gap: 20 }}>
              <div className="card">
                <h3 className="card-title" style={{ marginBottom: 16 }}>Medical Information</h3>
                <div style={{ display: 'flex', flexDirection: 'column', gap: 14 }}>
                  {[ { key: 'description', label: 'Description', rows: 3 }, { key: 'indications', label: 'Indications', rows: 3 }, { key: 'dosage', label: 'Dosage Instructions', rows: 3 }, { key: 'usage', label: 'Usage Instructions', rows: 3 }, { key: 'warnings', label: 'Warnings', rows: 2 }, { key: 'side_effects', label: 'Side Effects', rows: 2 }, { key: 'storage', label: 'Storage Instructions', rows: 2 }, { key: 'notes', label: 'Notes', rows: 2 } ].map(({ key, label, rows }) => (
                    <div key={key} className="form-group">
                      <label className="form-label">{label} <span className="form-label-optional">(optional)</span></label>
                      <textarea className="form-textarea" rows={rows} placeholder={`Enter ${label.toLowerCase()}...`} {...field(key as keyof MedicineUpdate)} />
                    </div>
                  ))}
                </div>
              </div>

              <div style={{ display: 'flex', gap: 10, justifyContent: 'flex-end' }}>
                <Link href={`/medicines/${id}`} className="btn btn-secondary">Cancel</Link>
                <button type="submit" className="btn btn-primary btn-lg" disabled={updateMutation.isPending}>
                  <Save size={16} />
                  {updateMutation.isPending ? 'Saving...' : 'Save Changes'}
                </button>
              </div>
            </div>
          </div>
        </form>
      </div>
    </div>
  );
}
