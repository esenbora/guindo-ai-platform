# GitHub Pages Deployment Setup

This project is configured to automatically deploy to GitHub Pages.

## Setup Instructions

1. **Enable GitHub Pages** in your repository:
   - Go to repository Settings → Pages
   - Under "Build and deployment":
     - Source: GitHub Actions

2. **Push changes** to the `main` branch:
   ```bash
   git add .
   git commit -m "Configure GitHub Pages deployment"
   git push origin main
   ```

3. **Wait for deployment**:
   - The GitHub Actions workflow will automatically build and deploy
   - Check the "Actions" tab to monitor progress
   - Once complete, your site will be available at:
     `https://esenbora.github.io/guindo-ai-platform/`

## Configuration Details

### Next.js Configuration
- **Static Export**: Configured with `output: 'export'`
- **Base Path**: Set to `/guindo-ai-platform` for GitHub Pages
- **Images**: Unoptimized for static export compatibility

### GitHub Actions Workflow
- **Trigger**: Automatically runs on push to `main` branch
- **Build Process**:
  1. Checks out code
  2. Sets up Node.js 20
  3. Installs dependencies
  4. Builds Next.js app
  5. Uploads build artifacts
  6. Deploys to GitHub Pages

## Local Development

To test the production build locally:

```bash
cd web/frontend
npm install
npm run build
npx serve out
```

## Important Notes

1. **API URLs**: Update `NEXT_PUBLIC_API_URL` in production if you have a backend API
2. **Environment Variables**: Add secrets in GitHub repository Settings → Secrets
3. **Custom Domain**: You can configure a custom domain in repository Settings → Pages

## Troubleshooting

- **Build Fails**: Check the Actions tab for error logs
- **404 Errors**: Ensure all links use the correct base path
- **Assets Not Loading**: Verify `basePath` is correctly configured in `next.config.js`
