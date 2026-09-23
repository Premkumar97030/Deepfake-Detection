import { useEffect, useRef } from "react";
import * as THREE from "three";
import { ShieldCheck, Cpu, Zap, Activity } from "lucide-react";

export default function Hero3DScanner() {
  const mountRef = useRef(null);

  useEffect(() => {
    const container = mountRef.current;
    if (!container) return;

    const width = container.clientWidth || 340;
    const height = container.clientHeight || 340;

    const scene = new THREE.Scene();
    const camera = new THREE.PerspectiveCamera(45, width / height, 0.1, 100);
    camera.position.set(0, 0, 8);

    const renderer = new THREE.WebGLRenderer({ alpha: true, antialias: true });
    renderer.setSize(width, height);
    renderer.setPixelRatio(Math.min(window.devicePixelRatio, 2));
    container.appendChild(renderer.domElement);

    // Group for entire 3D rig
    const group = new THREE.Group();
    scene.add(group);

    // 1. Core Glowing Icosahedron (Hologram Core)
    const icoGeo = new THREE.IcosahedronGeometry(2.1, 2);
    const icoMat = new THREE.MeshPhongMaterial({
      color: 0x4f46e5,
      emissive: 0x1e1b4b,
      wireframe: true,
      transparent: true,
      opacity: 0.65
    });
    const icoMesh = new THREE.Mesh(icoGeo, icoMat);
    group.add(icoMesh);

    // 2. Inner Solid Core with point light
    const innerGeo = new THREE.SphereGeometry(1.2, 24, 24);
    const innerMat = new THREE.MeshStandardMaterial({
      color: 0x00f0ff,
      emissive: 0x0066ff,
      roughness: 0.2,
      metalness: 0.8,
      transparent: true,
      opacity: 0.85
    });
    const innerMesh = new THREE.Mesh(innerGeo, innerMat);
    group.add(innerMesh);

    // 3. Surrounding 3D Gimbal Rings (Cyan & Violet)
    const createRing = (radius, tube, color, rotX, rotY) => {
      const ringGeo = new THREE.TorusGeometry(radius, tube, 16, 64);
      const ringMat = new THREE.MeshBasicMaterial({
        color,
        wireframe: true,
        transparent: true,
        opacity: 0.75
      });
      const ringMesh = new THREE.Mesh(ringGeo, ringMat);
      ringMesh.rotation.set(rotX, rotY, 0);
      return ringMesh;
    };

    const ring1 = createRing(2.8, 0.025, 0x00f0ff, Math.PI / 3, 0);
    const ring2 = createRing(3.1, 0.02, 0xa855f7, 0, Math.PI / 4);
    const ring3 = createRing(3.4, 0.015, 0x38bdf8, Math.PI / 2, Math.PI / 6);

    group.add(ring1);
    group.add(ring2);
    group.add(ring3);

    // 4. Scanning laser plane
    const planeGeo = new THREE.RingGeometry(0.1, 3.5, 32);
    const planeMat = new THREE.MeshBasicMaterial({
      color: 0x00ffcc,
      side: THREE.DoubleSide,
      transparent: true,
      opacity: 0.25
    });
    const scanPlane = new THREE.Mesh(planeGeo, planeMat);
    scanPlane.rotation.x = Math.PI / 2;
    group.add(scanPlane);

    // Lights
    const ambientLight = new THREE.AmbientLight(0xffffff, 0.8);
    scene.add(ambientLight);

    const pointLight = new THREE.PointLight(0x00f0ff, 3, 50);
    pointLight.position.set(5, 5, 5);
    scene.add(pointLight);

    const purpleLight = new THREE.PointLight(0x9333ea, 2, 50);
    purpleLight.position.set(-5, -5, 3);
    scene.add(purpleLight);

    // Interactive mouse rotation
    let targetRotationX = 0;
    let targetRotationY = 0;

    const handleMouseMove = (e) => {
      const rect = container.getBoundingClientRect();
      const x = ((e.clientX - rect.left) / width - 0.5) * 2;
      const y = ((e.clientY - rect.top) / height - 0.5) * 2;
      targetRotationY = x * 0.8;
      targetRotationX = y * 0.8;
    };

    container.addEventListener("mousemove", handleMouseMove);

    let animationId;
    const clock = new THREE.Clock();

    const animate = () => {
      animationId = requestAnimationFrame(animate);
      const t = clock.getElapsedTime();

      // Smooth rotate towards cursor + auto rotation
      group.rotation.y += (targetRotationY + t * 0.25 - group.rotation.y) * 0.05;
      group.rotation.x += (targetRotationX + Math.sin(t * 0.5) * 0.1 - group.rotation.x) * 0.05;

      // Gimbal animations
      ring1.rotation.z = t * 0.6;
      ring2.rotation.x = t * 0.4;
      ring3.rotation.y = -t * 0.5;

      // Scan plane vertical sweep
      scanPlane.position.y = Math.sin(t * 2) * 2.2;
      scanPlane.rotation.z = t * 0.3;

      // Core pulse
      const scale = 1 + Math.sin(t * 3) * 0.04;
      innerMesh.scale.set(scale, scale, scale);

      renderer.render(scene, camera);
    };

    animate();

    return () => {
      cancelAnimationFrame(animationId);
      container.removeEventListener("mousemove", handleMouseMove);
      if (container && renderer.domElement) {
        container.removeChild(renderer.domElement);
      }
      icoGeo.dispose();
      icoMat.dispose();
      innerGeo.dispose();
      innerMat.dispose();
      planeGeo.dispose();
      planeMat.dispose();
      renderer.dispose();
    };
  }, []);

  return (
    <div className="hero-3d-wrapper">
      <div className="hero-3d-hologram" ref={mountRef} />

      {/* Floating 3D HUD Indicators */}
      <div className="hud-badge top-left">
        <div className="hud-pulse-dot" />
        <div>
          <span className="hud-title">NEURAL SCANNER</span>
          <strong className="hud-val">ACTIVE 100 FPS</strong>
        </div>
      </div>

      <div className="hud-badge top-right">
        <Zap size={14} className="hud-icon cyan" />
        <div>
          <span className="hud-title">LATENCY</span>
          <strong className="hud-val">0.32s AVG</strong>
        </div>
      </div>

      <div className="hud-badge bottom-center">
        <ShieldCheck size={16} className="hud-icon emerald" />
        <div>
          <span className="hud-title">AUTHENTICITY ACCURACY</span>
          <strong className="hud-val">99.4% CONFIDENCE</strong>
        </div>
      </div>
    </div>
  );
}
