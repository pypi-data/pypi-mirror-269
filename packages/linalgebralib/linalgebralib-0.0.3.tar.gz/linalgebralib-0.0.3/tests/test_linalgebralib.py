import pytest
import sys
import math
sys.path.append('../')
from src.linalgebralib import LinAlgebraLib as la

class TestAddition:
    def test_column_matrix(self):
        c = la.Matrix(content=[[1],[2],[3]])
        a = la.columnVector(content=[1,2,3])
        b = a + c
        assert b == la.Matrix(content=[[2],[4],[6]])
    
    def test_matrix_column(self):
        c = la.Matrix(content=[[1],[2],[3]])
        a = la.columnVector(content=[1,2,3])
        b = c + a
        assert b == la.Matrix(content=[[2],[4],[6]])

    def test_row_matrix(self):
        b = la.rowVector(content=[1,2,3])
        d = la.Matrix(content=[[1,2,3]])
        a = b + d
        assert a == la.Matrix(content=[[2,4,6]])
    
    def test_matrix_row(self):
        b = la.rowVector(content=[1,2,3])
        d = la.Matrix(content=[[1,2,3]])
        a = d + b
        assert a == la.Matrix(content=[[2,4,6]])

    def test_row_column(self):
        a = la.columnVector(content=[1,2,3])
        b = la.rowVector(content=[1,2,3])
        with pytest.raises(TypeError):
            a + b
    
    def test_column_row(self):
        a = la.columnVector(content=[1,2,3])
        b = la.rowVector(content=[1,2,3])
        with pytest.raises(TypeError):
            a + b
    
    def test_matrix_row_mismatch(self):
        c = la.Matrix(content=[[1],[2],[3]])
        b = la.rowVector(content=[1,2,3])
        with pytest.raises(TypeError):
            c + b
    
    def test_row_matrix_mismatch(self):
        c = la.Matrix(content=[[1],[2],[3]])
        b = la.rowVector(content=[1,2,3])
        with pytest.raises(TypeError):
            b + c

    def test_column_matrix_mismatch(self):
        a = la.columnVector(content=[1,2,3])
        d = la.Matrix(content=[[1,2,3]])
        with pytest.raises(TypeError):
            a + d

    def test_matrix_column_mismatch(self):
        a = la.columnVector(content=[1,2,3])
        d = la.Matrix(content=[[1,2,3]])
        with pytest.raises(TypeError):
            d + a


class TestSubtraction:
    def test_column_matrix(self):
        c = la.Matrix(content=[[1],[2],[3]])
        a = la.columnVector(content=[1,2,3])
        b = a - c
        assert b == la.Matrix(content=[[0],[0],[0]])
    
    def test_matrix_column(self):
        c = la.Matrix(content=[[1],[2],[3]])
        a = la.columnVector(content=[1,2,3])
        b = c - a
        assert b == la.Matrix(content=[[0],[0],[0]])

    def test_row_matrix(self):
        b = la.rowVector(content=[1,2,3])
        d = la.Matrix(content=[[1,2,3]])
        a = b-d
        assert a == la.Matrix(content=[[0,0,0]])
    
    def test_matrix_row(self):
        b = la.rowVector(content=[1,2,3])
        d = la.Matrix(content=[[1,2,3]])
        a = d-b
        assert a == la.Matrix(content=[[0,0,0]])

    def test_row_column(self):
        a = la.columnVector(content=[1,2,3])
        b = la.rowVector(content=[1,2,3])
        with pytest.raises(TypeError):
            a - b
    
    def test_column_row(self):
        a = la.columnVector(content=[1,2,3])
        b = la.rowVector(content=[1,2,3])
        with pytest.raises(TypeError):
            a - b
    
    def test_matrix_row_mismatch(self):
        c = la.Matrix(content=[[1],[2],[3]])
        b = la.rowVector(content=[1,2,3])
        with pytest.raises(TypeError):
            c - b
    
    def test_row_matrix_mismatch(self):
        c = la.Matrix(content=[[1],[2],[3]])
        b = la.rowVector(content=[1,2,3])
        with pytest.raises(TypeError):
            b - c

    def test_column_matrix_mismatch(self):
        a = la.columnVector(content=[1,2,3])
        d = la.Matrix(content=[[1,2,3]])
        with pytest.raises(TypeError):
            a - d

    def test_matrix_column_mismatch(self):
        a = la.columnVector(content=[1,2,3])
        d = la.Matrix(content=[[1,2,3]])
        with pytest.raises(TypeError):
            d - a


class TestMultiplication:
    def test_two_valid_matrices(self):
        A = la.Matrix(content=[[1,2],[7,9]])
        B = la.Matrix(content=[[6,8,1],[1,2,1]])
        assert A*B == la.Matrix(content=[[8,12,3],[51,74,16]])
    def test_two_invalid_matrices(self):
        A = la.Matrix(content=[[1,2],[7,9]])
        B = la.Matrix(content=[[6,8,1],[1,2,1]])
        with pytest.raises(TypeError):
            B*A
    def test_valid_column_row(self):
        r = la.rowVector(content=[1,1,1])
        c = la.columnVector(content=[1,1,1,1])
        v = c*r
        assert v == la.Matrix(content=[[1,1,1],[1,1,1],[1,1,1],[1,1,1]])
    def test_valid_row_column(self):
        r = la.rowVector(content=[1,1,1])
        c = la.columnVector(content=[1,1,1])
        v = r*c
        assert v == la.Matrix(content=[[3]])

def test_transpose():
    A = la.Matrix(content=[[1,2,8],[7,0,1],[1,6,0]])
    assert A.transpose() == la.Matrix(content=[[1,7,1],[2,0,6],[8,1,0]])

def test_diagonal():
    A = la.Matrix(content=[[1,2,8],[7,0,1],[1,6,0]])
    assert A.diagonal()[0] == la.Matrix(content=[[1,2,8],[0,-14,-55],[0,0,-(166/7)]])

def test_ref():
    A = la.Matrix(content=[[1,2,8],[7,0,1],[1,6,0]])
    assert A.ref() == la.Matrix(content=[[1,2,8],[0,1,(55/14)],[0,0,1]])

def test_det():
    A = la.Matrix(content=[[2,4,5],[16,0,9],[1,1,7]])
    assert A.det() == -350

def test_inverse():
    A = la.Matrix(content=[[4,7],[2,6]])
    assert A.inverse() == la.Matrix(content=[[6/10,-7/10],[-2/10,4/10]])

def test_id_matrix():
    assert la.id_matrix(4) == la.Matrix(content=[[1,0,0,0],[0,1,0,0],[0,0,1,0],[0,0,0,1]])

def test_augment():
    A = la.Matrix(content=[[1,2],[2,3]])
    B = la.Matrix(content=[[0,0],[1,1]])
    assert la.augment(A,B) == la.Matrix(content=[[1,2,0,0],[2,3,1,1]])

def test_dot():
    A = la.columnVector(content=[3,4])
    assert la.dot(A,A) == 25

def test_magnitude():
    B = la.columnVector(content=[1,2,3,4])
    assert la.magnitude(B) == (30)**(0.5)

def test_angle():
    A = la.columnVector(content=[1,4])
    B = la.columnVector(content=[5,-1])
    assert la.angle(A, B) == math.acos(1/(442)**(0.5))