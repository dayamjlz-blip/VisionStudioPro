import cv2
import numpy as np
import pandas as pd
import streamlit as st

@st.cache_data
def to_grayscale(img): 
    return cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

@st.cache_data
def to_binary(img, threshold=128):
    _, binary = cv2.threshold(to_grayscale(img), threshold, 255, cv2.THRESH_BINARY)
    return binary

@st.cache_data
def arithmetic_ops(img, operation, value):
    f = img.astype(np.float32)
    if   operation == "Tambah (+)": res = cv2.add(f, value)
    elif operation == "Kurang (-)": res = cv2.subtract(f, value)
    elif operation == "Kali (×)":   res = cv2.multiply(f, value)
    elif operation == "Bagi (÷)":   res = cv2.divide(f, value)
    return np.clip(res, 0, 255).astype(np.uint8)

@st.cache_data
def logic_ops(img1, mask, operation):
    if operation == "NOT": return cv2.bitwise_not(img1)
    if operation == "AND": return cv2.bitwise_and(img1, mask)
    if operation == "OR":  return cv2.bitwise_or(img1, mask)
    if operation == "XOR": return cv2.bitwise_xor(img1, mask)

def plot_histogram(img):
    if len(img.shape) == 2:
        st.area_chart(pd.DataFrame(cv2.calcHist([img], [0], None, [256], [0, 256]).flatten(), columns=["Intensity"]), color="#4F46E5", height=200)
    else:
        data = { "Red": cv2.calcHist([img], [2], None, [256], [0, 256]).flatten(), "Green": cv2.calcHist([img], [1], None, [256], [0, 256]).flatten(), "Blue": cv2.calcHist([img], [0], None, [256], [0, 256]).flatten() }
        st.line_chart(pd.DataFrame(data), color=["#EF4444", "#10B981", "#3B82F6"], height=200)

@st.cache_data
def apply_filter(img, filter_type):
    if filter_type == "Gaussian Blur": return cv2.GaussianBlur(img, (9, 9), 0)
    elif filter_type == "Sharpening":  return cv2.filter2D(img, -1, np.array([[0,-1,0],[-1,5,-1],[0,-1,0]]))
    elif filter_type == "Sobel Edge":
        gray = to_grayscale(img)
        return cv2.magnitude(cv2.Sobel(gray, cv2.CV_64F, 1, 0, ksize=3), cv2.Sobel(gray, cv2.CV_64F, 0, 1, ksize=3)).astype(np.uint8)

@st.cache_data
def apply_morphology(img, operation, se_shape, se_size):
    _, binary = cv2.threshold(to_grayscale(img), 127, 255, cv2.THRESH_BINARY_INV)
    shapes = {"Persegi": cv2.MORPH_RECT, "Silang": cv2.MORPH_CROSS, "Elips": cv2.MORPH_ELLIPSE}
    se = cv2.getStructuringElement(shapes[se_shape], (se_size, se_size))
    if   operation == "Dilasi":  return cv2.dilate(binary, se, iterations=1)
    elif operation == "Erosi":   return cv2.erode(binary, se, iterations=1)
    elif operation == "Opening": return cv2.morphologyEx(binary, cv2.MORPH_OPEN, se)
    elif operation == "Closing": return cv2.morphologyEx(binary, cv2.MORPH_CLOSE, se)