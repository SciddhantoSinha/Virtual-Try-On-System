function updateARVisualization(height, weight, chest) {
    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(75, window.innerWidth / window.innerHeight, 0.1, 1000);
    const renderer = new THREE.WebGLRenderer();
    renderer.setSize(window.innerWidth, window.innerHeight);
    document.getElementById("arContainer").innerHTML = ""; // Clear existing canvas
    document.getElementById("arContainer").appendChild(renderer.domElement);

    const geometry = new THREE.BoxGeometry(chest / 50, height / 200, weight / 50);
    const material = new THREE.MeshBasicMaterial({ color: 0x00ff00 });
    const box = new THREE.Mesh(geometry, material);
    scene.add(box);

    camera.position.z = 5;

    function animate() {
        requestAnimationFrame(animate);
        box.rotation.x += 0.01;
        box.rotation.y += 0.01;
        renderer.render(scene, camera);
    }
    animate();
}
