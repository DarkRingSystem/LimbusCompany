# Knowledge Base Management System - Frontend

A modern Next.js-based frontend for managing knowledge bases with semantic search and retrieval testing capabilities.

## Features

- **Knowledge Base Management**: Create, read, update, and delete knowledge bases
- **Document Management**: Upload, organize, and manage documents within knowledge bases
- **Semantic Search**: Search documents using vector similarity
- **Retrieval Testing**: Test and evaluate retrieval effectiveness
- **Chunking Configuration**: Configure document chunking parameters
- **Responsive Design**: Mobile-friendly interface using Tailwind CSS

## Tech Stack

- **Framework**: Next.js 14
- **Language**: TypeScript
- **Styling**: Tailwind CSS
- **State Management**: Zustand
- **HTTP Client**: Axios
- **UI Components**: Lucide React Icons

## Prerequisites

- Node.js 18+ or npm 9+
- Backend API running on `http://localhost:8000`

## Installation

1. Install dependencies:
```bash
npm install
```

2. Configure environment variables in `.env.local`:
```
NEXT_PUBLIC_API_BASE_URL=http://localhost:8000/api
```

## Development

Start the development server:
```bash
npm run dev
```

The application will be available at `http://localhost:3000`

## Building

Build for production:
```bash
npm run build
npm start
```

## Project Structure

```
app/
├── layout.tsx              # Root layout
├── page.tsx                # Home page
├── globals.css             # Global styles
├── create/                 # Knowledge base creation
├── knowledge-bases/        # Knowledge base detail pages
└── components/             # Reusable components

lib/
├── api.ts                  # API client

public/                     # Static assets
```

## API Integration

The frontend communicates with the backend API at `http://localhost:8000/api`. Key endpoints:

- `POST /knowledge-bases` - Create knowledge base
- `GET /knowledge-bases` - List knowledge bases
- `GET /knowledge-bases/{id}` - Get knowledge base details
- `PUT /knowledge-bases/{id}` - Update knowledge base
- `DELETE /knowledge-bases/{id}` - Delete knowledge base
- `POST /documents/upload` - Upload documents
- `POST /search` - Search knowledge base
- `POST /preview-chunks` - Preview document chunks

## Configuration

### Tailwind CSS

Customize theme in `tailwind.config.js`

### Next.js

Configure Next.js in `next.config.js`

## Type Checking

Run TypeScript type checking:
```bash
npm run type-check
```

## Linting

Run ESLint:
```bash
npm run lint
```

## Notes

- This implementation focuses on knowledge base management functionality
- i18n (internationalization) and user management are not included
- Hybrid retrieval and Rerank features are reserved for future implementation

