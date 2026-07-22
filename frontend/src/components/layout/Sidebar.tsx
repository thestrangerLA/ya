'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';
import {
  Pill,
  ChevronRight,
} from 'lucide-react';
import { cn } from '@/lib/utils';

const navItems = [
  {
    section: 'การจัดการยาสัตว์',
    links: [
      { href: '/medicines', label: 'คลังเวชภัณฑ์ยา', icon: Pill },
    ],
  },
];

export function Sidebar() {
  const pathname = usePathname();

  function isActive(href: string) {
    if (href === '/') return pathname === '/';
    return pathname.startsWith(href);
  }

  return (
    <aside className="sidebar">
      {/* Logo */}
      <div className="sidebar-logo">
        <div style={{ display: 'flex', alignItems: 'center', gap: 10, marginBottom: 4 }}>
          <div
            style={{
              width: 34,
              height: 34,
              borderRadius: 9,
              background: 'linear-gradient(135deg, #16a34a, #22c55e)',
              display: 'flex',
              alignItems: 'center',
              justifyContent: 'center',
              fontSize: 18,
              flexShrink: 0,
            }}
          >
            🐾
          </div>
          <div>
            <h1>
              <span style={{ color: '#4ade80' }}>ระบบสารสนเทศ</span>
            </h1>
            <p style={{ fontSize: 11, color: '#9ca3af', marginTop: 1 }}>
              เวชภัณฑ์ยาสัตว์ (Animal Medicine)
            </p>
          </div>
        </div>
      </div>

      {/* Navigation */}
      <nav className="sidebar-nav">
        {navItems.map((section) => (
          <div key={section.section}>
            <p className="sidebar-section-label">{section.section}</p>
            {section.links.map(({ href, label, icon: Icon }) => (
              <Link
                key={href}
                href={href}
                className={cn('nav-item', isActive(href) && 'active')}
              >
                <Icon className="nav-icon" />
                <span style={{ flex: 1 }}>{label}</span>
                {isActive(href) && (
                  <ChevronRight size={14} style={{ opacity: 0.6 }} />
                )}
              </Link>
            ))}
          </div>
        ))}
      </nav>

      {/* Footer */}
      <div
        style={{
          padding: '16px 20px',
          borderTop: '1px solid #1f2937',
          fontSize: 11,
          color: '#6b7280',
        }}
      >
        <p>รุ่น 1.0.0 · ประมวลผลในเครื่อง</p>
        <p style={{ marginTop: 2 }}>© 2026 Animal Medicine IS</p>
      </div>
    </aside>
  );
}
