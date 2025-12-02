# Developer Portal - Quick Start Guide

## 🎉 Portal is Live!

Your developer portal is now running at: **http://localhost:3000/**

## 📁 Project Structure

```
portal/
├── src/
│   ├── components/           # UI components
│   │   ├── Header.jsx       # Top navigation bar
│   │   └── Sidebar.jsx      # Left sidebar menu
│   ├── pages/               # Main pages
│   │   ├── Overview.jsx     # Landing page with features
│   │   ├── Documentation.jsx # API reference docs
│   │   ├── ApiExplorer.jsx  # Interactive API testing
│   │   └── Authentication.jsx # Auth guide
│   ├── App.jsx              # Main app with routing
│   └── main.jsx             # Entry point
├── openapi.json             # Your OpenAPI spec
├── package.json             # Dependencies
└── vite.config.js          # Build config
```

## 🚀 Features Implemented

### 1. Overview Page (`/overview`)
- Hero section with API title and version
- Feature highlights (6 cards)
- Quick start code examples
- Resources list

### 2. Documentation Page (`/documentation`)
- Complete endpoint browser
- Filter by tags (auth, patrons, titles, copies, borrows, payments, users, webhooks)
- Expandable endpoint cards showing:
  - HTTP method and path
  - Description
  - Parameters (path, query, body)
  - Request schemas
  - Response codes
  - Authentication requirements

### 3. API Explorer (`/api-explorer`)
- Interactive endpoint testing
- Configurable base URL
- Bearer token authentication
- Dynamic form generation based on endpoint:
  - Path parameters
  - Query parameters
  - Request body editor (JSON)
- Real-time request execution
- Response viewer with status and body

### 4. Authentication Page (`/authentication`)
- Step-by-step auth guide
- Registration examples
- Login examples
- Token usage examples
- Security best practices
- Protected endpoints list
- Error handling info

## 🎨 Design Features

- **Modern UI**: Clean, professional design with custom color scheme
- **Responsive**: Works on desktop, tablet, and mobile
- **Method Colors**: 
  - GET: Blue (#61affe)
  - POST: Green (#49cc90)
  - PUT: Orange (#fca130)
  - PATCH: Cyan (#50e3c2)
  - DELETE: Red (#f93e3e)
- **Code Highlighting**: Dark code blocks for better readability
- **Interactive Elements**: Hover effects, expandable sections, active states

## 🛠️ Technologies Used

- **React 18** - Modern UI framework
- **React Router 6** - Client-side routing
- **Vite** - Lightning-fast build tool
- **Axios** - HTTP client for API requests
- **React Icons** - Beautiful icon set
- **Pure CSS** - Custom styling (no framework bloat)

## 📝 How to Use

### Testing API Endpoints

1. Navigate to **API Explorer**
2. Set your API base URL (default: `http://localhost:5000/api/v4`)
3. If needed, add your JWT token from logging in
4. Select an endpoint from the list
5. Fill in any required parameters
6. Click "Execute Request"
7. View the response

### Example: Login Flow

1. Go to API Explorer
2. Find `POST /auth/login`
3. Enter request body:
```json
{
  "email": "user@example.com",
  "password": "your-password"
}
```
4. Execute and copy the returned `accessToken`
5. Paste token in the "Authorization Token" field
6. Now you can test protected endpoints!

## 🔧 Customization

### Change Base URL
Edit the default in `src/pages/ApiExplorer.jsx`:
```javascript
const [baseUrl, setBaseUrl] = useState('YOUR_API_URL');
```

### Update Branding
Edit `src/components/Header.jsx` to change:
- Logo text
- Version badge
- Links

### Modify Colors
Edit CSS variables in `src/index.css`:
```css
:root {
  --primary-color: #2563eb;
  --success-color: #10b981;
  /* etc. */
}
```

## 📦 Deployment

### Build for Production
```bash
npm run build
```

### Deploy to Static Hosting
Upload the `dist/` folder to:
- Netlify
- Vercel
- GitHub Pages
- AWS S3
- Any static hosting service

## 🐛 Troubleshooting

### CORS Errors
If you get CORS errors when testing endpoints:
- Ensure your API has CORS enabled
- Add your portal URL to API's allowed origins
- For development, use a CORS proxy or configure your API

### Port Already in Use
Change the port in `vite.config.js`:
```javascript
server: {
  port: 3001, // Change this
}
```

## 📚 Next Steps

1. **Connect to Real API**: Update base URL to your actual API
2. **Test Endpoints**: Try all endpoints in API Explorer
3. **Customize Styling**: Match your brand colors
4. **Add Features**: Consider adding:
   - Response history
   - Request collection saving
   - Code generation (curl, fetch, axios)
   - Dark mode toggle
   - Search functionality

## 💡 Tips

- Use the tag filters in Documentation to quickly find related endpoints
- Save your JWT token in the API Explorer for easier testing
- Check the Authentication page for security best practices
- The portal reads directly from your `openapi.json` file - any updates will reflect automatically

Enjoy your new developer portal! 🎉
