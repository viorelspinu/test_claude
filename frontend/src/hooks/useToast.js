import { useState, useCallback } from 'react';

function useToast() {
  const [toasts, setToasts] = useState([]);

  const addToast = useCallback((message, type = 'error', duration = 5000) => {
    const id = Date.now() + Math.random();
    const newToast = { id, message, type, duration };
    
    setToasts(prev => [...prev, newToast]);
    
    return id;
  }, []);

  const removeToast = useCallback((id) => {
    setToasts(prev => prev.filter(toast => toast.id !== id));
  }, []);

  const showError = useCallback((message) => {
    return addToast(message, 'error');
  }, [addToast]);

  const showSuccess = useCallback((message) => {
    return addToast(message, 'success', 3000);
  }, [addToast]);

  const showWarning = useCallback((message) => {
    return addToast(message, 'warning', 4000);
  }, [addToast]);

  const showInfo = useCallback((message) => {
    return addToast(message, 'info', 4000);
  }, [addToast]);

  const clearAllToasts = useCallback(() => {
    setToasts([]);
  }, []);

  return {
    toasts,
    addToast,
    removeToast,
    showError,
    showSuccess,
    showWarning,
    showInfo,
    clearAllToasts
  };
}

export default useToast;