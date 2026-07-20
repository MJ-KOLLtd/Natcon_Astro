export interface ResourceDriveLink {
  id: string;
  label: string;
  href: string;
  tone: 'gold' | 'blue' | 'green';
  actionLabel: string;
}

export const CONFERENCE_PROGRAM_URL = 'https://bit.ly/18thCELINatConProgram';

export const SPONSOR_RESOURCES_DRIVE =
  'https://drive.google.com/drive/folders/1MOghX_zN6oCD3Vw3hlWwm45jJzC7xgQ1?usp=sharing';

export const SPEAKER_RESOURCES_DRIVE =
  'https://drive.google.com/drive/folders/1S1ISBt37Kcbte5d63KM2vqD-ej_7YneI?usp=sharing';

export const resourceDriveLinks: ResourceDriveLink[] = [
  {
    id: 'program',
    label: 'Conference Program',
    href: CONFERENCE_PROGRAM_URL,
    tone: 'green',
    actionLabel: 'Open program',
  },
  {
    id: 'sponsor-resources',
    label: 'Sponsor Resources',
    href: SPONSOR_RESOURCES_DRIVE,
    tone: 'gold',
    actionLabel: 'Open folder',
  },
  {
    id: 'speaker-resources',
    label: 'Speaker Resources',
    href: SPEAKER_RESOURCES_DRIVE,
    tone: 'blue',
    actionLabel: 'Open folder',
  },
];

export const resourceNavLinks = resourceDriveLinks.map((item) => ({
  label: item.label,
  href: `#cel-nc-resources-${item.id}`,
}));
