import pytest
import subprocess

if __name__ == '__main__':
    # pytest.main(['-vs','-k',"test_payment"])
    # pytest.main(['-vs','--alluredir','./report/xml',"TestCase/test_payment_creditCard.py",'--clean-alluredir'])
    pytest.main(['-vs','--alluredir','./report/xml','--clean-alluredir'])
