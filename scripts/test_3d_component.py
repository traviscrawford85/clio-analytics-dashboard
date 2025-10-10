#!/usr/bin/env python3
"""
Test script for the 3D Matter Analytics Dashboard

This script tests the 3D matter visualization component and services
to ensure they're working correctly with the CFE Solutions integration.
"""

import sys
import os
from pathlib import Path

# Add the dashboard to Python path
dashboard_root = Path(__file__).parent
sys.path.insert(0, str(dashboard_root))

def test_3d_service():
    """Test the 3D matter analytics service."""
    print("🧪 Testing 3D Matter Analytics Service...")
    
    try:
        from dash_clio_dashboard.services.matter_3d_analytics import matter_3d_service
        
        # Test data generation
        print("   • Testing data generation...")
        data = matter_3d_service.get_matter_3d_data(limit=50)
        
        if data and len(data.get('departments', [])) > 0:
            print(f"   ✅ Generated {len(data['departments'])} matter data points")
            print(f"   ✅ Departments: {set(data['departments'])}")
            print(f"   ✅ Expense range: ${min(data['total_expenses']):,.0f} - ${max(data['total_expenses']):,.0f}")
        else:
            print("   ❌ No data generated")
            return False
            
        # Test department summary
        print("   • Testing department summary...")
        summary = matter_3d_service.get_department_summary()
        
        if summary and len(summary.get('departments', [])) > 0:
            print(f"   ✅ Department summary for {len(summary['departments'])} departments")
        else:
            print("   ⚠️  Department summary using mock data")
            
        return True
        
    except Exception as e:
        print(f"   ❌ Service test failed: {e}")
        return False

def test_layout_import():
    """Test that the 3D layout can be imported."""
    print("🧪 Testing 3D Layout Import...")
    
    try:
        from dash_clio_dashboard.layouts.matter_3d import create_matter_3d_layout
        
        print("   • Creating layout...")
        layout = create_matter_3d_layout()
        
        if layout:
            print("   ✅ Layout created successfully")
            return True
        else:
            print("   ❌ Layout creation failed")
            return False
            
    except Exception as e:
        print(f"   ❌ Layout import failed: {e}")
        return False

def test_app_integration():
    """Test that the app can run with 3D integration."""
    print("🧪 Testing App Integration...")
    
    try:
        from dash_clio_dashboard.app import app
        
        print("   • App imported successfully")
        
        # Test that the app server can be accessed
        if hasattr(app, 'server'):
            print("   ✅ App server available")
            return True
        else:
            print("   ❌ App server not available")
            return False
            
    except Exception as e:
        print(f"   ❌ App integration test failed: {e}")
        return False

def run_comprehensive_test():
    """Run all tests and provide summary."""
    print("🚀 Starting 3D Matter Analytics Component Tests\n")
    
    tests = [
        ("3D Analytics Service", test_3d_service),
        ("3D Layout Import", test_layout_import),
        ("App Integration", test_app_integration)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            results.append((test_name, result))
            print()
        except Exception as e:
            print(f"   ❌ {test_name} crashed: {e}\n")
            results.append((test_name, False))
    
    # Summary
    print("="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    passed = 0
    total = len(results)
    
    for test_name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{status} {test_name}")
        if result:
            passed += 1
    
    print(f"\nResults: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! 3D Matter Analytics is ready.")
        print("\nNext steps:")
        print("1. Run the dashboard: python dash_clio_dashboard/app.py")
        print("2. Navigate to the '3D Matter View' tab")
        print("3. Explore the interactive 3D visualization")
        return True
    else:
        print("⚠️  Some tests failed. Check the errors above.")
        return False

if __name__ == "__main__":
    success = run_comprehensive_test()
    sys.exit(0 if success else 1)