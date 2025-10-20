# Git-Komet Frontend

Frontend application for the Git-Komet team effectiveness analysis system.

## Tech Stack

- **Nuxt.js 3** - Vue.js framework
- **Vue.js 3** - Progressive JavaScript framework
- **TypeScript** - Type-safe JavaScript
- **Nuxt UI** - UI component library
- **Chart.js + vue-chartjs** - Data visualization

## Setup

1. Install dependencies:
```bash
npm install
# or
yarn install
# or
pnpm install
```

2. Set up environment variables:
Create a `.env` file in the frontend directory:
```
API_BASE_URL=http://localhost:8000/api/v1
```

3. Run development server:
```bash
npm run dev
```

The application will be available at http://localhost:3000

## Build for Production

```bash
npm run build
```

## Generate Static Site

```bash
npm run generate
```

## Project Structure

```
frontend/
├── assets/
│   └── css/               # Global styles
├── components/            # Vue components
├── composables/           # Composable functions (API calls, etc.)
├── layouts/               # Page layouts
├── pages/                 # Application pages
│   ├── index.vue         # Dashboard
│   ├── repositories.vue  # Repository management
│   ├── teams.vue         # Team management
│   └── metrics.vue       # Metrics & analytics
├── plugins/               # Nuxt plugins
├── public/                # Static files
├── nuxt.config.ts        # Nuxt configuration
├── package.json          # Dependencies
└── tsconfig.json         # TypeScript configuration
```

## Features

- 📊 **Dashboard** - Overview of system statistics
- 📦 **Repository Management** - Add and manage Git repositories
- 👥 **Team Management** - Create and manage development teams
- 📈 **Metrics & Analytics** - Visualize team effectiveness metrics
- 🎨 **Responsive Design** - Works on all devices
- ⚡ **Fast Performance** - Built with Nuxt.js for optimal speed

## Pages

### Dashboard (`/`)
Main overview page showing system statistics and quick actions.

### Repositories (`/repositories`)
Manage Git repositories for analysis. Add repositories, sync commits, and view repository details.

### Teams (`/teams`)
Manage development teams. Create teams, add members, and track team composition.

### Metrics (`/metrics`)
View and analyze team effectiveness metrics through visualizations and charts.

## API Integration

The frontend communicates with the backend API using the `useApi` composable, which provides functions for:
- Fetching and creating repositories
- Managing teams and team members
- Retrieving metrics and analytics

## Development

To add new features:
1. Create new pages in the `pages/` directory
2. Add components in the `components/` directory
3. Use the `useApi` composable for API calls
4. Style components using scoped CSS

## Environment Variables

- `API_BASE_URL` - Backend API base URL (default: http://localhost:8000/api/v1)
