'use client';
import { useState } from 'react';
import Image from 'next/image';
import { Star } from 'lucide-react';
import type { MedicineImage } from '@/types';
import { getImageUrl } from '@/lib/utils';

export function ImageGallery({ images, onSetPrimary, onDelete }: {
  images: MedicineImage[];
  onSetPrimary?: (imageId: string) => void;
  onDelete?: (imageId: string) => void;
}) {
  const [selected, setSelected] = useState(0);
  if (images.length === 0) {
    return (
      <div style={{ aspectRatio: '1/1', background: '#f9fafb', borderRadius: 12, border: '1px solid #e5e7eb', display: 'flex', alignItems: 'center', justifyContent: 'center', fontSize: 48 }}>
        💊
      </div>
    );
  }
  const current = images[selected];
  return (
    <div style={{ display: 'flex', flexDirection: 'column', gap: 10 }}>
      <div style={{ position: 'relative', aspectRatio: '1/1', borderRadius: 12, overflow: 'hidden', border: '1px solid #e5e7eb', background: '#f9fafb' }}>
        <img src={getImageUrl(current.url)} alt="Medicine" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
        {current.is_primary && (
          <span style={{ position: 'absolute', top: 8, left: 8, background: '#16a34a', color: '#fff', padding: '2px 8px', borderRadius: 999, fontSize: 11, fontWeight: 700 }}>PRIMARY</span>
        )}
      </div>
      {images.length > 1 && (
        <div style={{ display: 'flex', gap: 6, flexWrap: 'wrap' }}>
          {images.map((img, i) => (
            <div key={img.id} onClick={() => setSelected(i)} style={{ width: 64, height: 64, borderRadius: 8, overflow: 'hidden', cursor: 'pointer', border: i === selected ? '2px solid #16a34a' : '2px solid transparent', transition: 'border-color 0.15s' }}>
              <img src={getImageUrl(img.url)} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
