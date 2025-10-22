const { spawn } = require('child_process');
const path = require('path');

// Build the frontend first
console.log('🔨 Building frontend...');
const build = spawn('npm', ['run', 'build'], {
  cwd: __dirname,
  stdio: 'inherit',
  shell: true
});

build.on('close', (code) => {
  if (code === 0) {
    console.log('✅ Build completed successfully');
    console.log('🚀 Starting preview server...');
    
    // Start the preview server
    const preview = spawn('npm', ['run', 'preview'], {
      cwd: __dirname,
      stdio: 'inherit',
      shell: true
    });
    
    preview.on('close', (code) => {
      console.log(`Preview server exited with code ${code}`);
    });
  } else {
    console.error('❌ Build failed');
    process.exit(1);
  }
});
