"""
STRESS TEST SUITE FOR BOIDS SWARM SIMULATION
============================================

Tests the performance and stability of the Boids swarm under extreme conditions.
Measures FPS, memory usage, and behavioral consistency.

Author: HFjr65™ (Håkon Fløstad Jr.)
License: MIT
"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.spatial import cKDTree
import time
import psutil
import os

class StressTestBoids:
    """Stress test framework for Boids swarm simulation."""
    
    def __init__(self):
        self.results = {}
        self.process = psutil.Process(os.getpid())
    
    def stress_test_scaling(self, particle_counts=[100, 300, 600, 1000, 2000, 5000]):
        """Test performance scaling with particle count."""
        print("\n" + "="*70)
        print("STRESS TEST 1: PARTICLE COUNT SCALING")
        print("="*70)
        
        timings = []
        fps_results = []
        memory_results = []
        
        for n_particles in particle_counts:
            print(f"\nTesting N = {n_particles} particles...")
            
            # Initialize
            positions = np.random.rand(n_particles, 2) * 25.0
            angles = (np.random.rand(n_particles) - 0.5) * 2 * np.pi
            
            # Warm-up
            tree = cKDTree(positions, boxsize=25.0)
            _ = tree.query_ball_point(positions, r=4.0)
            
            # Measure 50 frames
            times = []
            for frame in range(50):
                start = time.perf_counter()
                
                tree = cKDTree(positions, boxsize=25.0)
                neighbors_list = tree.query_ball_point(positions, r=4.0)
                
                for i in range(n_particles):
                    idxs = [idx for idx in neighbors_list[i] if idx != i]
                    if idxs:
                        delta = positions[idxs] - positions[i]
                        delta = delta - 25.0 * np.round(delta / 25.0)
                        dists = np.hypot(delta[:, 0], delta[:, 1])
                        angles[i] = np.arctan2(np.mean(delta[:, 1]), np.mean(delta[:, 0]))
                
                positions += np.column_stack([np.cos(angles), np.sin(angles)]) * 0.12
                positions %= 25.0
                
                end = time.perf_counter()
                times.append(end - start)
            
            avg_frame_time = np.mean(times)
            fps = 1.0 / avg_frame_time if avg_frame_time > 0 else 0
            
            # Memory
            mem_usage = self.process.memory_info().rss / 1024 / 1024  # MB
            
            timings.append(avg_frame_time)
            fps_results.append(fps)
            memory_results.append(mem_usage)
            
            print(f"  ✓ Avg frame time: {avg_frame_time*1000:.2f} ms")
            print(f"  ✓ FPS: {fps:.1f}")
            print(f"  ✓ Memory: {mem_usage:.1f} MB")
        
        self.results['scaling'] = {
            'particle_counts': particle_counts,
            'timings': timings,
            'fps': fps_results,
            'memory': memory_results
        }
        
        return particle_counts, fps_results, timings, memory_results
    
    def stress_test_radius_sensitivity(self, n_particles=1000, radii=[0.5, 1.0, 2.0, 4.0, 8.0]):
        """Test performance sensitivity to interaction radius."""
        print("\n" + "="*70)
        print("STRESS TEST 2: INTERACTION RADIUS SENSITIVITY")
        print("="*70)
        
        positions = np.random.rand(n_particles, 2) * 25.0
        angles = (np.random.rand(n_particles) - 0.5) * 2 * np.pi
        
        radius_times = []
        radius_neighbor_counts = []
        
        for radius in radii:
            print(f"\nTesting radius = {radius}...")
            
            times = []
            neighbor_counts = []
            
            for _ in range(50):
                start = time.perf_counter()
                
                tree = cKDTree(positions, boxsize=25.0)
                neighbors_list = tree.query_ball_point(positions, r=radius)
                
                neighbor_counts.append(np.mean([len(n) for n in neighbors_list]))
                
                end = time.perf_counter()
                times.append(end - start)
            
            avg_time = np.mean(times)
            avg_neighbors = np.mean(neighbor_counts)
            
            radius_times.append(avg_time)
            radius_neighbor_counts.append(avg_neighbors)
            
            print(f"  ✓ Query time: {avg_time*1000:.3f} ms")
            print(f"  ✓ Avg neighbors per particle: {avg_neighbors:.1f}")
        
        self.results['radius'] = {
            'radii': radii,
            'times': radius_times,
            'neighbor_counts': radius_neighbor_counts
        }
        
        return radii, radius_times, radius_neighbor_counts
    
    def stress_test_neighbor_search_methods(self, n_particles=1000, n_queries=100):
        """Compare cKDTree vs naive neighbor search."""
        print("\n" + "="*70)
        print("STRESS TEST 3: NEIGHBOR SEARCH METHOD COMPARISON")
        print("="*70)
        
        positions = np.random.rand(n_particles, 2) * 25.0
        radius = 4.0
        
        # cKDTree method
        print(f"\nMethod 1: cKDTree (N={n_particles})...")
        times_kdtree = []
        for _ in range(n_queries):
            start = time.perf_counter()
            tree = cKDTree(positions, boxsize=25.0)
            _ = tree.query_ball_point(positions, r=radius)
            times_kdtree.append(time.perf_counter() - start)
        
        avg_kdtree = np.mean(times_kdtree)
        print(f"  ✓ cKDTree: {avg_kdtree*1000:.3f} ms/query")
        
        # Naive method (brute force)
        print(f"\nMethod 2: Naive brute force (N={n_particles})...")
        times_naive = []
        for _ in range(n_queries):
            start = time.perf_counter()
            for i in range(n_particles):
                pos_i = positions[i]
                for j in range(n_particles):
                    if i != j:
                        delta = positions[j] - pos_i
                        delta = delta - 25.0 * np.round(delta / 25.0)
                        dist = np.hypot(delta[0], delta[1])
                        if dist < radius:
                            pass  # Found neighbor
            times_naive.append(time.perf_counter() - start)
        
        avg_naive = np.mean(times_naive)
        speedup = avg_naive / avg_kdtree
        print(f"  ✓ Naive: {avg_naive*1000:.3f} ms/query")
        print(f"  ✓ SPEEDUP: {speedup:.1f}x faster with cKDTree")
        
        self.results['method_comparison'] = {
            'kdtree_ms': avg_kdtree * 1000,
            'naive_ms': avg_naive * 1000,
            'speedup': speedup
        }
        
        return avg_kdtree, avg_naive, speedup
    
    def stress_test_stability_long_run(self, n_particles=600, frames=500):
        """Test stability and memory leaks over long simulation."""
        print("\n" + "="*70)
        print("STRESS TEST 4: LONG-RUN STABILITY (500 frames)")
        print("="*70)
        
        positions = np.random.rand(n_particles, 2) * 25.0
        angles = (np.random.rand(n_particles) - 0.5) * 2 * np.pi
        
        frame_times = []
        memory_timeline = []
        order_parameter = []
        
        for frame in range(frames):
            start = time.perf_counter()
            
            tree = cKDTree(positions, boxsize=25.0)
            neighbors_list = tree.query_ball_point(positions, r=4.0)
            
            for i in range(n_particles):
                idxs = [idx for idx in neighbors_list[i] if idx != i]
                if idxs:
                    delta = positions[idxs] - positions[i]
                    delta = delta - 25.0 * np.round(delta / 25.0)
                    angles[i] = np.arctan2(np.mean(delta[:, 1]), np.mean(delta[:, 0]))
                    angles[i] += (np.random.rand() - 0.5) * 0.15
            
            positions += np.column_stack([np.cos(angles), np.sin(angles)]) * 0.12
            positions %= 25.0
            
            # Compute order parameter
            order = np.hypot(np.mean(np.cos(angles)), np.mean(np.sin(angles)))
            order_parameter.append(order)
            
            frame_times.append(time.perf_counter() - start)
            mem = self.process.memory_info().rss / 1024 / 1024
            memory_timeline.append(mem)
            
            if (frame + 1) % 100 == 0:
                print(f"  Frame {frame+1}: {frame_times[-1]*1000:.2f} ms, Memory: {mem:.1f} MB, Order: {order:.3f}")
        
        avg_fps = 1.0 / np.mean(frame_times)
        mem_stability = np.std(memory_timeline)
        
        print(f"\n✓ Average FPS: {avg_fps:.1f}")
        print(f"✓ Memory stability (std dev): {mem_stability:.2f} MB")
        print(f"✓ Final order parameter: {order_parameter[-1]:.3f}")
        print(f"✓ No crashes detected!")
        
        self.results['stability'] = {
            'frames': frames,
            'avg_fps': avg_fps,
            'memory_stability': mem_stability,
            'final_order': order_parameter[-1],
            'memory_timeline': memory_timeline,
            'order_timeline': order_parameter
        }
        
        return frame_times, memory_timeline, order_parameter
    
    def plot_results(self):
        """Generate summary plots."""
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        fig.suptitle('HFjr65™ Boids Swarm — Stress Test Results', fontsize=14, fontweight='bold')
        
        # Plot 1: Scaling
        if 'scaling' in self.results:
            r = self.results['scaling']
            axes[0, 0].plot(r['particle_counts'], r['fps'], 'o-', linewidth=2, markersize=8)
            axes[0, 0].set_xlabel('Number of Particles')
            axes[0, 0].set_ylabel('FPS')
            axes[0, 0].set_title('FPS vs Particle Count')
            axes[0, 0].grid(True, alpha=0.3)
            axes[0, 0].set_xscale('log')
        
        # Plot 2: Memory
        if 'scaling' in self.results:
            r = self.results['scaling']
            axes[0, 1].plot(r['particle_counts'], r['memory'], 's-', color='green', linewidth=2, markersize=8)
            axes[0, 1].set_xlabel('Number of Particles')
            axes[0, 1].set_ylabel('Memory (MB)')
            axes[0, 1].set_title('Memory Usage vs Particle Count')
            axes[0, 1].grid(True, alpha=0.3)
            axes[0, 1].set_xscale('log')
        
        # Plot 3: Radius sensitivity
        if 'radius' in self.results:
            r = self.results['radius']
            ax3_twin = axes[1, 0].twinx()
            line1 = axes[1, 0].plot(r['radii'], r['times'], 'o-', color='blue', linewidth=2, markersize=8, label='Query Time')
            line2 = ax3_twin.plot(r['radii'], r['neighbor_counts'], 's-', color='red', linewidth=2, markersize=8, label='Avg Neighbors')
            axes[1, 0].set_xlabel('Interaction Radius')
            axes[1, 0].set_ylabel('Query Time (s)', color='blue')
            ax3_twin.set_ylabel('Avg Neighbors', color='red')
            axes[1, 0].set_title('Radius Sensitivity')
            axes[1, 0].grid(True, alpha=0.3)
            axes[1, 0].tick_params(axis='y', labelcolor='blue')
            ax3_twin.tick_params(axis='y', labelcolor='red')
        
        # Plot 4: Stability
        if 'stability' in self.results:
            r = self.results['stability']
            axes[1, 1].plot(r['order_timeline'], linewidth=1.5, alpha=0.8)
            axes[1, 1].fill_between(range(len(r['order_timeline'])), r['order_timeline'], alpha=0.3)
            axes[1, 1].set_xlabel('Frame')
            axes[1, 1].set_ylabel('Order Parameter')
            axes[1, 1].set_title(f'Long-Run Stability ({len(r["order_timeline"])} frames)')
            axes[1, 1].grid(True, alpha=0.3)
            axes[1, 1].set_ylim([0, 1])
        
        plt.tight_layout()
        plt.savefig('stress_test_results.png', dpi=150, bbox_inches='tight')
        print("\n✓ Results saved to 'stress_test_results.png'")
        plt.show()
    
    def print_summary(self):
        """Print comprehensive test summary."""
        print("\n" + "="*70)
        print("STRESS TEST SUMMARY — HFjr65™ Boids Swarm")
        print("="*70)
        
        if 'scaling' in self.results:
            r = self.results['scaling']
            print("\n📊 SCALING RESULTS:")
            for n, fps, mem in zip(r['particle_counts'], r['fps'], r['memory']):
                print(f"   {n:5d} particles: {fps:6.1f} FPS, {mem:6.1f} MB")
        
        if 'method_comparison' in self.results:
            r = self.results['method_comparison']
            print(f"\n⚡ METHOD COMPARISON:")
            print(f"   cKDTree: {r['kdtree_ms']:.3f} ms/query")
            print(f"   Naive:   {r['naive_ms']:.3f} ms/query")
            print(f"   SPEEDUP: {r['speedup']:.1f}x")
        
        if 'stability' in self.results:
            r = self.results['stability']
            print(f"\n🔄 STABILITY TEST ({r['frames']} frames):")
            print(f"   Average FPS: {r['avg_fps']:.1f}")
            print(f"   Memory stability: ±{r['memory_stability']:.2f} MB")
            print(f"   Final order parameter: {r['final_order']:.3f}")
            print(f"   Status: ✅ PASSED (No crashes)")
        
        print("\n" + "="*70 + "\n")

def run_full_stress_test():
    """Execute all stress tests."""
    print("\n")
    print("╔" + "="*68 + "╗")
    print("║" + " "*68 + "║")
    print("║" + "  HFjr65™ BOIDS SWARM STRESS TEST SUITE".center(68) + "║")
    print("║" + "  Computational Physics & Visualization Pipeline".center(68) + "║")
    print("║" + " "*68 + "║")
    print("╚" + "="*68 + "╝")
    
    tester = StressTestBoids()
    
    # Run all tests
    tester.stress_test_scaling(particle_counts=[100, 300, 600, 1000, 2000, 5000])
    tester.stress_test_radius_sensitivity(n_particles=1000, radii=[0.5, 1.0, 2.0, 4.0, 8.0])
    tester.stress_test_neighbor_search_methods(n_particles=1000, n_queries=100)
    tester.stress_test_stability_long_run(n_particles=600, frames=500)
    
    # Print summary and plot
    tester.print_summary()
    tester.plot_results()

if __name__ == "__main__":
    run_full_stress_test()
