// API client configuration for Todo List Application
// Base configuration for communicating with Flask backend

// Determine API base URL based on environment and proxy settings
const getApiBaseUrl = () => {
  // In production, use the same origin
  if (process.env.NODE_ENV === 'production') {
    return '/api';
  }
  
  // In development with proxy (package.json proxy setting), use relative path
  if (process.env.REACT_APP_USE_PROXY !== 'false') {
    return '/api';
  }
  
  // Use environment variable if set
  if (process.env.REACT_APP_API_URL) {
    return process.env.REACT_APP_API_URL;
  }
  
  // Default to localhost:5001 for development
  return 'http://localhost:5001/api';
};

const API_BASE_URL = getApiBaseUrl();

// API client class to handle HTTP requests
class ApiClient {
  constructor(baseURL = API_BASE_URL) {
    this.baseURL = baseURL;
    this.defaultHeaders = {
      'Content-Type': 'application/json',
    };
    this.pendingRequests = new Map(); // Track pending requests to prevent duplicates
    this.requestThrottle = 100; // Minimum delay between requests in ms
    this.lastRequestTime = 0;
  }

  // Generic request method with error handling
  async request(endpoint, options = {}) {
    const url = `${this.baseURL}${endpoint}`;
    const requestKey = `${options.method || 'GET'}:${url}:${JSON.stringify(options.body || {})}`;
    
    // Prevent duplicate requests
    if (this.pendingRequests.has(requestKey)) {
      console.warn('Duplicate request prevented:', requestKey);
      return this.pendingRequests.get(requestKey);
    }
    
    // Throttle requests
    const now = Date.now();
    if (now - this.lastRequestTime < this.requestThrottle) {
      await new Promise(resolve => setTimeout(resolve, this.requestThrottle));
    }
    this.lastRequestTime = Date.now();
    
    const config = {
      headers: { ...this.defaultHeaders, ...options.headers },
      ...options,
    };

    const requestPromise = this._executeRequest(url, config, requestKey);
    this.pendingRequests.set(requestKey, requestPromise);
    
    try {
      const result = await requestPromise;
      return result;
    } finally {
      this.pendingRequests.delete(requestKey);
    }
  }
  
  async _executeRequest(url, config, requestKey) {
    try {
      const response = await fetch(url, config);
      
      // Handle different response status codes according to API contract
      if (response.status === 204) {
        // No Content - successful delete
        return null;
      }

      const data = await response.json();

      if (!response.ok) {
        // Handle API error responses
        throw new ApiError(
          data.error?.message || 'An error occurred',
          response.status,
          data.error?.code || 'UNKNOWN_ERROR',
          data.error?.details || {}
        );
      }

      return data;
    } catch (error) {
      if (error instanceof ApiError) {
        throw error;
      }
      
      // Handle network errors
      throw new ApiError(
        'Network error occurred. Please check your connection.',
        0,
        'NETWORK_ERROR',
        { originalError: error.message }
      );
    }
  }

  // GET request
  async get(endpoint, params = {}) {
    const searchParams = new URLSearchParams();
    Object.keys(params).forEach(key => {
      if (params[key] !== undefined && params[key] !== null) {
        searchParams.append(key, params[key]);
      }
    });

    const queryString = searchParams.toString();
    const fullEndpoint = queryString ? `${endpoint}?${queryString}` : endpoint;

    return this.request(fullEndpoint, { method: 'GET' });
  }

  // POST request
  async post(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'POST',
      body: JSON.stringify(data),
    });
  }

  // PUT request
  async put(endpoint, data = {}) {
    return this.request(endpoint, {
      method: 'PUT',
      body: JSON.stringify(data),
    });
  }

  // DELETE request
  async delete(endpoint) {
    return this.request(endpoint, { method: 'DELETE' });
  }
}

// Custom error class for API errors
class ApiError extends Error {
  constructor(message, status, code, details = {}) {
    super(message);
    this.name = 'ApiError';
    this.status = status;
    this.code = code;
    this.details = details;
  }

  // Check if error is a specific type
  isValidationError() {
    return this.status === 400 || this.status === 422;
  }

  isNotFoundError() {
    return this.status === 404;
  }

  isServerError() {
    return this.status >= 500;
  }

  isNetworkError() {
    return this.status === 0;
  }
}

// Create singleton instance
const apiClient = new ApiClient();

export { apiClient, ApiError };
export default apiClient;