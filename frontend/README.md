# Image Tagging API Dashboard

A professional SvelteKit frontend dashboard for the Image Tagging API service.

## Features

- 🔑 API Key Authentication
- 📊 Dashboard with usage statistics
- 🏷️ Image tagging playground
- 📈 Usage history tracking
- 💅 Responsive design with TailwindCSS
- 📱 Mobile-friendly UI

## Tech Stack

- **Framework**: SvelteKit
- **Language**: TypeScript
- **Styling**: TailwindCSS
- **Routing**: svelte-spa-router
- **Package Manager**: yarn

## Prerequisites

- Node.js 18+
- yarn package manager

## Installation

```bash
cd frontend
yarn install
```

## Environment Setup

Copy `.env.example` to `.env.local` and update the values:

```bash
cp .env.example .env.local
```

Edit `.env.local`:

```env
# Backend API URL (update if backend runs on different port)
VITE_API_BASE_URL=http://localhost:8000
```

## Development

```bash
yarn dev
```

The dashboard will be available at `http://localhost:5173`.

## Production Build

```bash
yarn build
yarn preview
```

## Architecture

### Directory Structure

```
frontend/
├── src/
│   ├── components/        # Reusable Svelte components
│   ├── lib/              # Utilities and API client
│   ├── pages/            # Page components (routed)
│   ├── stores/           # Svelte stores for state management
│   ├── styles/           # Global CSS and styling
│   ├── types/            # TypeScript type definitions
│   ├── app.svelte        # Root component with routing
│   └── main.ts           # Entry point
├── index.html            # HTML template
├── package.json          # Dependencies
├── tsconfig.json         # TypeScript config
├── vite.config.ts        # Vite build config
└── tailwind.config.js    # TailwindCSS config
```

### Key Components

- **LoginPage.svelte**: API key authentication
- **Dashboard.svelte**: Main dashboard with overview
- **Tagger.svelte**: Image tagging playground
- **UsageTable.svelte**: Usage history visualization
- **Sidebar.svelte**: Navigation menu

### State Management

Utilizes Svelte stores for:
- Authentication state (`authStore`)
- Usage data (`usageStore`)

### API Client

Centralized API client in `src/lib/api.ts`:
- `validateApiKey()`: Authenticate with API key
- `tagImage()`: Submit image for tagging
- `getUsageHistory()`: Fetch usage statistics

## Usage

### 1. Login

1. Navigate to the login page
2. Enter your API key
3. Click "Enter Dashboard"

### 2. Dashboard

View:
- Your masked API key
- Weekly quota and remaining requests
- Quota consumption progress bar
- Last usage timestamp

### 3. Image Tagger

1. Enter an image URL
2. Select tagging mode (fast, reasoning, advanced_reasoning)
3. Click "Run Tagger"
4. View RAW JSON response from the API
5. Toggle between raw and formatted views

### 4. Usage History

View a paginated table of:
- Request timestamps
- API endpoints
- Response status codes

## API Integration

### Endpoints Used

```
GET  /api/v1/health/          - Validate API key
POST /api/v1/tag/             - Tag an image
GET  /api/v1/usage/           - Get usage history (TODO in backend)
```

### Authentication

API key is sent via `Authorization` header:

```
Authorization: Api-Key <your-api-key>
```

## Error Handling

- Invalid API key → "Invalid API key."
- Quota exceeded → "API quota exceeded."
- Network errors → Graceful error messages
- Form validation → Real-time feedback

## Development Notes

### TypeScript

All code is written in TypeScript with strict type checking. Run type checking:

```bash
yarn check
```

### Styling

Utilizes TailwindCSS utility classes. No CSS-in-JS or component scoping needed beyond standard Svelte scoping.

### Responsive Design

Mobile-first approach with breakpoints:
- `sm`: 640px
- `lg`: 1024px
- `xl`: 1280px

## Future Enhancements

- [ ] Implement `/api/v1/usage/` endpoint in backend
- [ ] Add usage analytics charts
- [ ] Implement billing/subscription UI
- [ ] Add dark mode support
- [ ] Batch image tagging
- [ ] Image preview before tagging
- [ ] Export usage reports (CSV/PDF)

## Troubleshooting

### CORS Issues

If you get CORS errors, ensure the backend has CORS enabled for `http://localhost:5173`.

### API Connection Issues

1. Check backend is running: `http://localhost:8000/api/v1/health/`
2. Update `VITE_API_BASE_URL` in `.env.local` if backend runs on different port
3. Check browser console for network errors

## License

MIT
