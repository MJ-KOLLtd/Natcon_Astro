export interface ResourceDriveLink {
  id: string;
  label: string;
  href: string;
  tone: 'gold' | 'blue';
}

export const SPONSOR_VIDEOS_DRIVE =
  'https://drive.google.com/drive/folders/1qEFXcw0-Mg07udeTIqAODnV7x7asVwaM?usp=sharing';

export const PARTNER_BROCHURES_DRIVE =
  'https://drive.google.com/drive/folders/1eWjWibY9W7UzWsf6jSkUL4G-U1MeFEIO?usp=sharing';

export const resourceDriveLinks: ResourceDriveLink[] = [
  {
    id: 'sponsor-videos',
    label: 'Sponsor presentations',
    href: SPONSOR_VIDEOS_DRIVE,
    tone: 'gold',
  },
  {
    id: 'partner-brochures',
    label: 'Partner brochures',
    href: PARTNER_BROCHURES_DRIVE,
    tone: 'blue',
  },
];

export const resourceNavLinks = resourceDriveLinks.map((item) => ({
  label: item.label,
  href: `#cel-nc-resources-${item.id}`,
}));