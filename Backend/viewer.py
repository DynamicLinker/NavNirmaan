import http.server
import socketserver
import os

HTML_CONTENT = """
<!DOCTYPE html>
<html>
  <head>
    <title>3D House Viewer</title>
    <!-- We use A-Frame, a WebVR framework that provides native First Person 'Walking' controls -->
    <script src="https://aframe.io/releases/1.4.0/aframe.min.js"></script>
  </head>
  <body>
    <a-scene>
      <a-assets>
        <a-asset-item id="house" src="interactive.glb"></a-asset-item>
      </a-assets>
      
      <!-- Load the exported House Model -->
      <a-entity gltf-model="#house"></a-entity>
      
      <!-- First Person Player Camera -->
      <!-- A-Frame converts Blender's +Y to WebGL's -Z. So Blender (20, 15) becomes A-Frame (20, -15) -->
      <!-- We enable Pointer Lock so when you click the screen, you can look around like a video game -->
      <a-entity position="20 1.6 -15">
        <a-camera look-controls="pointerLockEnabled: true" wasd-controls="acceleration: 30"></a-camera>
      </a-entity>
      
    </a-scene>
    

  </body>
</html>
"""

def main():
    # 1. Write the HTML file to the directory
    html_path = "index.html"
    with open(html_path, "w") as f:
        f.write(HTML_CONTENT)
    
    # 2. Start a simple web server
    port = 8000
    Handler = http.server.SimpleHTTPRequestHandler
    
    print("=" * 60)
    print(f" Web Server started at:  http://localhost:{port}")
    print("=" * 60)
    
    # Avoid "Address already in use" errors if restarted quickly
    socketserver.TCPServer.allow_reuse_address = True
    
    with socketserver.TCPServer(("", port), Handler) as httpd:
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\\nShutting down server.")

if __name__ == "__main__":
    main()
