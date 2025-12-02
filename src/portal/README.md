# API Developer Portal

A modern, interactive developer portal built with React for the Library Management API.

## Features

- 📚 **Interactive API Documentation** - Browse all available endpoints with detailed parameter and schema information
- 🔍 **API Explorer** - Test API endpoints directly from the browser with authentication support
- 🔐 **Authentication Guide** - Complete guide on how to authenticate and use Bearer tokens
- 📖 **Comprehensive Overview** - Learn about all available resources and quick start examples
- 🎨 **Modern UI** - Clean, responsive design that works on all devices

## Getting Started

### Prerequisites

- Node.js 16+ and npm

### Installation

1. Clone or navigate to the project directory:
```bash
cd /home/lam/Desktop/UET/SoA/portal
```

2. Install dependencies:
```bash
npm install
```

3. Start the development server:
```bash
npm run dev
```

The portal will open automatically at `http://localhost:3000`

## Available Scripts

- `npm run dev` - Start development server
- `npm run build` - Build for production
- `npm run preview` - Preview production build locally

## Project Structure

```
portal/
├── src/
│   ├── components/        # Reusable components
│   │   ├── Header.jsx
│   │   ├── Sidebar.jsx
│   │   └── *.css
│   ├── pages/            # Page components
│   │   ├── Overview.jsx
│   │   ├── Documentation.jsx
│   │   ├── ApiExplorer.jsx
│   │   ├── Authentication.jsx
│   │   └── *.css
│   ├── App.jsx           # Main app component
│   ├── main.jsx          # Entry point
│   └── index.css         # Global styles
├── openapi.json          # OpenAPI specification
├── index.html
├── vite.config.js
└── package.json
```

## Usage

### Overview Page
Get started with an overview of the API, including:
- Feature highlights
- Quick start examples
- Available resources

### Documentation Page
Browse the complete API documentation:
- Filter endpoints by tag
- View request/response schemas
- See parameter requirements
- Check authentication needs

### API Explorer
Test API endpoints interactively:
1. Configure the base URL (default: `http://localhost:5000/api/v4`)
2. Add your JWT Bearer token (if needed)
3. Select an endpoint from the list
4. Fill in path/query parameters
5. Edit the request body (for POST/PUT/PATCH)
6. Click "Execute Request" to see the response

### Authentication Page
Learn how to:
- Register a user account
- Login and get JWT tokens
- Use tokens in API requests
- Follow security best practices

## API Configuration

To connect to your API:

1. Update the base URL in the API Explorer
2. For development, ensure your API is running (e.g., `http://localhost:5000`)
3. For production, update the base URL to your production API endpoint

## Building for Production

```bash
npm run build
```

The built files will be in the `dist/` directory, ready to deploy to any static hosting service.

## Technologies Used

- **React 18** - UI framework
- **React Router** - Client-side routing
- **Vite** - Build tool and dev server
- **Axios** - HTTP client for API requests
- **React Icons** - Icon library
- **Prism.js** - Syntax highlighting

## License

MIT

## Support

For issues or questions about the API, please refer to the documentation or contact the API team.
