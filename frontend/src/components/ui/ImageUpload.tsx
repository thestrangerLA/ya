'use client';
import { useCallback, useState } from 'react';
import { useDropzone } from 'react-dropzone';
import { Upload, X, Star } from 'lucide-react';
import { getImageUrl } from '@/lib/utils';

interface UploadedFile {
  file: File;
  preview: string;
  isPrimary: boolean;
}

export function ImageUpload({
  onFilesChange,
  maxFiles = 10,
  existingImages = [],
  onDeleteExisting,
}: {
  onFilesChange: (files: File[]) => void;
  maxFiles?: number;
  existingImages?: Array<{ id: string; url: string | null; is_primary: boolean }>;
  onDeleteExisting?: (id: string) => void;
}) {
  const [files, setFiles] = useState<UploadedFile[]>([]);

  const onDrop = useCallback((accepted: File[]) => {
    const newFiles = accepted.map((file, i) => ({
      file,
      preview: URL.createObjectURL(file),
      isPrimary: files.length === 0 && existingImages.length === 0 && i === 0,
    }));
    const updated = [...files, ...newFiles].slice(0, maxFiles);
    setFiles(updated);
    onFilesChange(updated.map(f => f.file));
  }, [files, existingImages, maxFiles, onFilesChange]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: { 'image/jpeg': [], 'image/png': [], 'image/webp': [] },
    maxFiles,
  });

  const removeFile = (i: number) => {
    const updated = files.filter((_, idx) => idx !== i);
    setFiles(updated);
    onFilesChange(updated.map(f => f.file));
  };

  return (
    <div>
      <div {...getRootProps()} className={`dropzone${isDragActive ? ' dragover' : ''}`}>
        <input {...getInputProps()} />
        <Upload size={32} style={{ margin: '0 auto', color: '#9ca3af' }} />
        <p className="dropzone-text">
          {isDragActive ? 'Drop files here...' : 'Drag & drop images here, or click to select'}
        </p>
        <p style={{ fontSize: 12, color: '#9ca3af', marginTop: 4 }}>JPEG, PNG, WebP — up to {maxFiles} images</p>
      </div>

      {(existingImages.length > 0 || files.length > 0) && (
        <div className="image-preview-grid">
          {existingImages.map(img => (
            <div key={img.id} className={`image-preview-item${img.is_primary ? ' primary' : ''}`}>
              <img src={getImageUrl(img.url)} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              {img.is_primary && <span style={{ position: 'absolute', bottom: 4, left: 4, fontSize: 10, background: '#16a34a', color: '#fff', padding: '1px 5px', borderRadius: 999 }}>Primary</span>}
              {onDeleteExisting && (
                <button className="image-preview-delete" onClick={() => onDeleteExisting(img.id)}>
                  <X size={10} />
                </button>
              )}
            </div>
          ))}
          {files.map((f, i) => (
            <div key={i} className={`image-preview-item${f.isPrimary ? ' primary' : ''}`}>
              <img src={f.preview} alt="" style={{ width: '100%', height: '100%', objectFit: 'cover' }} />
              {f.isPrimary && <span style={{ position: 'absolute', bottom: 4, left: 4, fontSize: 10, background: '#16a34a', color: '#fff', padding: '1px 5px', borderRadius: 999 }}>Primary</span>}
              <button className="image-preview-delete" onClick={() => removeFile(i)}>
                <X size={10} />
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
