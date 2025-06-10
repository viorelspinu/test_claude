import { useState, useCallback } from 'react';
import { ApiError } from '../services/api.js';
import { MESSAGES } from '../utils/constants.js';

/**
 * Custom hook for managing API call states and error handling
 * Provides loading, error, and success states for API operations
 */
const useApi = () => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [data, setData] = useState(null);

  // Execute an API call with automatic state management
  const execute = useCallback(async (apiCall, options = {}) => {
    const { 
      loadingMessage = null,
      successMessage = null,
      errorMessage = null,
      onSuccess = null,
      onError = null,
      resetDataOnStart = true 
    } = options;

    setLoading(true);
    setError(null);
    
    if (resetDataOnStart) {
      setData(null);
    }

    try {
      const result = await apiCall();
      setData(result);
      setLoading(false);
      
      if (successMessage) {
        console.log(successMessage);
      }
      
      if (onSuccess) {
        onSuccess(result);
      }
      
      return result;
    } catch (err) {
      console.error('API call failed:', err);
      
      let errorMsg = errorMessage || MESSAGES.ERROR_GENERIC;
      
      if (err instanceof ApiError) {
        if (err.isNetworkError()) {
          errorMsg = MESSAGES.ERROR_NETWORK;
        } else if (err.message) {
          errorMsg = err.message;
        }
      } else if (err.message) {
        errorMsg = err.message;
      }
      
      setError(errorMsg);
      setLoading(false);
      
      if (onError) {
        onError(err);
      }
      
      throw err; // Re-throw to allow caller to handle if needed
    }
  }, []);

  // Reset all states
  const reset = useCallback(() => {
    setLoading(false);
    setError(null);
    setData(null);
  }, []);

  // Clear error state
  const clearError = useCallback(() => {
    setError(null);
  }, []);

  // Set loading state manually
  const setLoadingState = useCallback((isLoading) => {
    setLoading(isLoading);
  }, []);

  return {
    loading,
    error,
    data,
    execute,
    reset,
    clearError,
    setLoadingState
  };
};

/**
 * Custom hook for managing multiple concurrent API calls
 * Useful for operations like bulk updates or parallel data fetching
 */
export const useApiMultiple = () => {
  const [loadingStates, setLoadingStates] = useState({});
  const [errorStates, setErrorStates] = useState({});
  const [dataStates, setDataStates] = useState({});

  const execute = useCallback(async (key, apiCall, options = {}) => {
    const { 
      onSuccess = null,
      onError = null,
      resetDataOnStart = true 
    } = options;

    setLoadingStates(prev => ({ ...prev, [key]: true }));
    setErrorStates(prev => ({ ...prev, [key]: null }));
    
    if (resetDataOnStart) {
      setDataStates(prev => ({ ...prev, [key]: null }));
    }

    try {
      const result = await apiCall();
      
      setDataStates(prev => ({ ...prev, [key]: result }));
      setLoadingStates(prev => ({ ...prev, [key]: false }));
      
      if (onSuccess) {
        onSuccess(result);
      }
      
      return result;
    } catch (err) {
      console.error(`API call failed for ${key}:`, err);
      
      let errorMsg = MESSAGES.ERROR_GENERIC;
      
      if (err instanceof ApiError) {
        if (err.isNetworkError()) {
          errorMsg = MESSAGES.ERROR_NETWORK;
        } else if (err.message) {
          errorMsg = err.message;
        }
      } else if (err.message) {
        errorMsg = err.message;
      }
      
      setErrorStates(prev => ({ ...prev, [key]: errorMsg }));
      setLoadingStates(prev => ({ ...prev, [key]: false }));
      
      if (onError) {
        onError(err);
      }
      
      throw err;
    }
  }, []);

  const reset = useCallback((key) => {
    if (key) {
      setLoadingStates(prev => ({ ...prev, [key]: false }));
      setErrorStates(prev => ({ ...prev, [key]: null }));
      setDataStates(prev => ({ ...prev, [key]: null }));
    } else {
      setLoadingStates({});
      setErrorStates({});
      setDataStates({});
    }
  }, []);

  const clearError = useCallback((key) => {
    setErrorStates(prev => ({ ...prev, [key]: null }));
  }, []);

  const isLoading = useCallback((key) => {
    return key ? loadingStates[key] || false : Object.values(loadingStates).some(Boolean);
  }, [loadingStates]);

  const getError = useCallback((key) => {
    return errorStates[key] || null;
  }, [errorStates]);

  const getData = useCallback((key) => {
    return dataStates[key] || null;
  }, [dataStates]);

  return {
    execute,
    reset,
    clearError,
    isLoading,
    getError,
    getData,
    loadingStates,
    errorStates,
    dataStates
  };
};

/**
 * Custom hook for debounced API calls
 * Useful for search functionality or auto-save features
 */
export const useDebouncedApi = (delay = 300) => {
  const [debounceTimer, setDebounceTimer] = useState(null);
  const api = useApi();

  const debouncedExecute = useCallback((apiCall, options = {}) => {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
    }

    const timer = setTimeout(() => {
      api.execute(apiCall, options);
    }, delay);

    setDebounceTimer(timer);
  }, [api, delay, debounceTimer]);

  const cancelDebounce = useCallback(() => {
    if (debounceTimer) {
      clearTimeout(debounceTimer);
      setDebounceTimer(null);
    }
  }, [debounceTimer]);

  return {
    ...api,
    debouncedExecute,
    cancelDebounce,
    isDebouncing: !!debounceTimer
  };
};

export default useApi;