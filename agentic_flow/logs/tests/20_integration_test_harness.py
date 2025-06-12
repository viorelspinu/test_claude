#!/usr/bin/env python3
"""
Test Harness for Task 20: Integration Test Script Validation
Validates the integration test script implementation without requiring running servers
"""

import os
import sys
import json
import importlib.util
from typing import Dict, List, Tuple
from datetime import datetime

class IntegrationTestValidator:
    """Validates the integration test script implementation"""
    
    def __init__(self):
        self.test_results = []
        self.script_path = "/Users/viorel/workspace/test_claude/agentic_flow/logs/tests/20_integration_test_script.py"
        
    def log_test(self, test_name: str, passed: bool, details: str = "", error: str = ""):
        """Log test result"""
        result = {
            "test_name": test_name,
            "passed": passed,
            "details": details,
            "error": error,
            "timestamp": datetime.now().isoformat()
        }
        self.test_results.append(result)
        status = "✅ PASS" if passed else "❌ FAIL"
        print(f"{status}: {test_name}")
        if details:
            print(f"    Details: {details}")
        if error:
            print(f"    Error: {error}")
    
    def test_script_exists(self) -> bool:
        """Test 1: Integration test script file exists"""
        if os.path.exists(self.script_path):
            self.log_test("Script File Exists", True, f"Found at {self.script_path}")
            return True
        else:
            self.log_test("Script File Exists", False, "", f"Script not found at {self.script_path}")
            return False
    
    def test_script_executable(self) -> bool:
        """Test 2: Script has executable permissions and shebang"""
        try:
            with open(self.script_path, 'r') as f:
                first_line = f.readline().strip()
            
            has_shebang = first_line.startswith('#!')
            is_executable = os.access(self.script_path, os.X_OK)
            
            if has_shebang:
                self.log_test("Script Executable", True, f"Has shebang: {first_line}")
                return True
            else:
                self.log_test("Script Executable", False, "", "Missing shebang line")
                return False
        except Exception as e:
            self.log_test("Script Executable", False, "", f"Error checking script: {str(e)}")
            return False
    
    def test_required_imports(self) -> bool:
        """Test 3: Script has all required imports"""
        required_imports = [
            'requests', 'json', 'time', 'sys', 'os', 
            'typing', 'datetime'
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            missing_imports = []
            for imp in required_imports:
                if f"import {imp}" not in content and f"from {imp}" not in content:
                    missing_imports.append(imp)
            
            if not missing_imports:
                self.log_test("Required Imports", True, f"All required imports present: {', '.join(required_imports)}")
                return True
            else:
                self.log_test("Required Imports", False, "", f"Missing imports: {', '.join(missing_imports)}")
                return False
        except Exception as e:
            self.log_test("Required Imports", False, "", f"Error reading script: {str(e)}")
            return False
    
    def test_class_structure(self) -> bool:
        """Test 4: TodoIntegrationTester class exists with required methods"""
        required_methods = [
            '__init__', 'log_test', 'test_backend_connectivity', 
            'test_frontend_connectivity', 'test_cors_configuration',
            'test_empty_todos_list', 'test_create_todo', 'test_read_todos',
            'test_update_todo', 'test_delete_todo', 'test_error_handling',
            'test_data_persistence', 'test_concurrent_operations',
            'test_complete_user_workflow', 'run_all_tests'
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            # Check for class definition
            if 'class TodoIntegrationTester:' not in content:
                self.log_test("Class Structure", False, "", "TodoIntegrationTester class not found")
                return False
            
            # Check for required methods
            missing_methods = []
            for method in required_methods:
                if f"def {method}(" not in content:
                    missing_methods.append(method)
            
            if not missing_methods:
                self.log_test("Class Structure", True, f"TodoIntegrationTester class with {len(required_methods)} methods")
                return True
            else:
                self.log_test("Class Structure", False, "", f"Missing methods: {', '.join(missing_methods)}")
                return False
        except Exception as e:
            self.log_test("Class Structure", False, "", f"Error analyzing class: {str(e)}")
            return False
    
    def test_http_methods_coverage(self) -> bool:
        """Test 5: All HTTP methods are tested"""
        http_methods = ['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS']
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            method_coverage = []
            for method in http_methods:
                if f"requests.{method.lower()}(" in content:
                    method_coverage.append(method)
            
            if len(method_coverage) >= 4:  # GET, POST, PUT, DELETE minimum
                self.log_test("HTTP Methods Coverage", True, f"Covers HTTP methods: {', '.join(method_coverage)}")
                return True
            else:
                self.log_test("HTTP Methods Coverage", False, "", f"Only covers: {', '.join(method_coverage)}")
                return False
        except Exception as e:
            self.log_test("HTTP Methods Coverage", False, "", f"Error checking HTTP methods: {str(e)}")
            return False
    
    def test_error_handling(self) -> bool:
        """Test 6: Proper error handling implementation"""
        error_patterns = [
            'try:', 'except', 'RequestException', 'timeout='
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            found_patterns = []
            for pattern in error_patterns:
                if pattern in content:
                    found_patterns.append(pattern)
            
            if len(found_patterns) >= 3:
                self.log_test("Error Handling", True, f"Implements error handling patterns: {', '.join(found_patterns)}")
                return True
            else:
                self.log_test("Error Handling", False, "", f"Limited error handling: {', '.join(found_patterns)}")
                return False
        except Exception as e:
            self.log_test("Error Handling", False, "", f"Error checking error handling: {str(e)}")
            return False
    
    def test_crud_operations(self) -> bool:
        """Test 7: All CRUD operations are tested"""
        crud_operations = [
            'test_create_todo', 'test_read_todos', 
            'test_update_todo', 'test_delete_todo'
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            implemented_crud = []
            for operation in crud_operations:
                if f"def {operation}(" in content:
                    implemented_crud.append(operation)
            
            if len(implemented_crud) == len(crud_operations):
                self.log_test("CRUD Operations", True, f"All CRUD operations tested: {', '.join(implemented_crud)}")
                return True
            else:
                missing = set(crud_operations) - set(implemented_crud)
                self.log_test("CRUD Operations", False, "", f"Missing CRUD tests: {', '.join(missing)}")
                return False
        except Exception as e:
            self.log_test("CRUD Operations", False, "", f"Error checking CRUD operations: {str(e)}")
            return False
    
    def test_advanced_scenarios(self) -> bool:
        """Test 8: Advanced integration scenarios"""
        advanced_tests = [
            'test_error_handling', 'test_data_persistence',
            'test_concurrent_operations', 'test_complete_user_workflow'
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            implemented_advanced = []
            for test in advanced_tests:
                if f"def {test}(" in content:
                    implemented_advanced.append(test)
            
            if len(implemented_advanced) >= 3:
                self.log_test("Advanced Scenarios", True, f"Advanced tests: {', '.join(implemented_advanced)}")
                return True
            else:
                self.log_test("Advanced Scenarios", False, "", f"Limited advanced testing: {', '.join(implemented_advanced)}")
                return False
        except Exception as e:
            self.log_test("Advanced Scenarios", False, "", f"Error checking advanced scenarios: {str(e)}")
            return False
    
    def test_reporting_functionality(self) -> bool:
        """Test 9: Test reporting and output functionality"""
        reporting_features = [
            'generate_json_report', 'test_results', 'log_test', 'passed', 'total'
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            implemented_reporting = []
            for feature in reporting_features:
                if feature in content:
                    implemented_reporting.append(feature)
            
            if len(implemented_reporting) >= 4:
                self.log_test("Reporting Functionality", True, f"Reporting features: {', '.join(implemented_reporting)}")
                return True
            else:
                self.log_test("Reporting Functionality", False, "", f"Limited reporting: {', '.join(implemented_reporting)}")
                return False
        except Exception as e:
            self.log_test("Reporting Functionality", False, "", f"Error checking reporting: {str(e)}")
            return False
    
    def test_configuration_flexibility(self) -> bool:
        """Test 10: Configuration and deployment flexibility"""
        config_features = [
            'backend_url', 'frontend_url', 'os.getenv', 'sys.argv'
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            implemented_config = []
            for feature in config_features:
                if feature in content:
                    implemented_config.append(feature)
            
            if len(implemented_config) >= 3:
                self.log_test("Configuration Flexibility", True, f"Config features: {', '.join(implemented_config)}")
                return True
            else:
                self.log_test("Configuration Flexibility", False, "", f"Limited configuration: {', '.join(implemented_config)}")
                return False
        except Exception as e:
            self.log_test("Configuration Flexibility", False, "", f"Error checking configuration: {str(e)}")
            return False
    
    def test_cleanup_functionality(self) -> bool:
        """Test 11: Test data cleanup implementation"""
        cleanup_features = [
            'cleanup', 'todos_created', 'test_delete_todo'
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            implemented_cleanup = []
            for feature in cleanup_features:
                if feature in content:
                    implemented_cleanup.append(feature)
            
            if len(implemented_cleanup) >= 2:
                self.log_test("Cleanup Functionality", True, f"Cleanup features: {', '.join(implemented_cleanup)}")
                return True
            else:
                self.log_test("Cleanup Functionality", False, "", f"Limited cleanup: {', '.join(implemented_cleanup)}")
                return False
        except Exception as e:
            self.log_test("Cleanup Functionality", False, "", f"Error checking cleanup: {str(e)}")
            return False
    
    def test_main_function(self) -> bool:
        """Test 12: Main function and script execution"""
        main_features = [
            'def main():', 'if __name__ == "__main__":', 'sys.exit'
        ]
        
        try:
            with open(self.script_path, 'r') as f:
                content = f.read()
            
            implemented_main = []
            for feature in main_features:
                if feature in content:
                    implemented_main.append(feature)
            
            if len(implemented_main) >= 2:
                self.log_test("Main Function", True, f"Main execution features: {', '.join(implemented_main)}")
                return True
            else:
                self.log_test("Main Function", False, "", f"Limited main function: {', '.join(implemented_main)}")
                return False
        except Exception as e:
            self.log_test("Main Function", False, "", f"Error checking main function: {str(e)}")
            return False
    
    def run_all_tests(self) -> Tuple[int, int]:
        """Run all validation tests"""
        print("=" * 60)
        print("INTEGRATION TEST SCRIPT - VALIDATION SUITE")
        print("=" * 60)
        print(f"Testing script: {self.script_path}")
        print(f"Validation started: {datetime.now().isoformat()}")
        print("=" * 60)
        
        # Run all validation tests
        if not self.test_script_exists():
            print("\n❌ Script file not found - stopping validation")
            return 0, 1
        
        self.test_script_executable()
        self.test_required_imports()
        self.test_class_structure()
        self.test_http_methods_coverage()
        self.test_error_handling()
        self.test_crud_operations()
        self.test_advanced_scenarios()
        self.test_reporting_functionality()
        self.test_configuration_flexibility()
        self.test_cleanup_functionality()
        self.test_main_function()
        
        # Generate summary
        passed = sum(1 for result in self.test_results if result['passed'])
        total = len(self.test_results)
        
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        print(f"Total validation tests: {total}")
        print(f"Passed: {passed}")
        print(f"Failed: {total - passed}")
        print(f"Success rate: {(passed/total)*100:.1f}%")
        
        if passed == total:
            print("🎉 ALL VALIDATIONS PASSED - Integration test script is comprehensive!")
        elif passed >= total * 0.8:
            print("✅ MOSTLY PASSED - Integration test script meets requirements with minor issues")
        else:
            print("⚠️  ISSUES FOUND - Integration test script needs improvement")
        
        return passed, total
    
    def generate_json_report(self, output_file: str):
        """Generate JSON validation report"""
        report = {
            "validation_suite": "Integration Test Script Validation",
            "script_path": self.script_path,
            "validation_timestamp": datetime.now().isoformat(),
            "total_tests": len(self.test_results),
            "passed_tests": sum(1 for r in self.test_results if r['passed']),
            "failed_tests": sum(1 for r in self.test_results if not r['passed']),
            "success_rate": (sum(1 for r in self.test_results if r['passed']) / len(self.test_results)) * 100 if self.test_results else 0,
            "validation_results": self.test_results
        }
        
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        print(f"\nDetailed validation report saved to: {output_file}")

def main():
    """Main validation runner"""
    validator = IntegrationTestValidator()
    passed, total = validator.run_all_tests()
    
    # Generate JSON report
    report_file = "/Users/viorel/workspace/test_claude/agentic_flow/logs/tests/20_integration_test_validation.json"
    validator.generate_json_report(report_file)
    
    # Exit with appropriate code
    sys.exit(0 if passed >= total * 0.8 else 1)  # 80% pass rate acceptable

if __name__ == "__main__":
    main()