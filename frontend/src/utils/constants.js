// Application constants for Todo List App
// Following the API contract specifications from parallel_dev_sync.md

export const PRIORITIES = {
  HIGH: 'High',
  MEDIUM: 'Medium',
  LOW: 'Low'
};

export const PRIORITY_OPTIONS = [
  { value: PRIORITIES.HIGH, label: 'High', color: '#c62828' },
  { value: PRIORITIES.MEDIUM, label: 'Medium', color: '#ef6c00' },
  { value: PRIORITIES.LOW, label: 'Low', color: '#2e7d32' }
];

export const SORT_OPTIONS = {
  CREATED_AT: 'created_at',
  UPDATED_AT: 'updated_at',
  TITLE: 'title',
  PRIORITY: 'priority'
};

export const SORT_ORDER = {
  ASC: 'asc',
  DESC: 'desc'
};

export const API_ENDPOINTS = {
  TASKS: '/tasks',
  TASK_BY_ID: (id) => `/tasks/${id}`,
  TASK_STATS: '/tasks/stats'
};

export const HTTP_STATUS = {
  OK: 200,
  CREATED: 201,
  NO_CONTENT: 204,
  BAD_REQUEST: 400,
  NOT_FOUND: 404,
  UNPROCESSABLE_ENTITY: 422,
  INTERNAL_SERVER_ERROR: 500
};

export const ERROR_CODES = {
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  NETWORK_ERROR: 'NETWORK_ERROR',
  NOT_FOUND: 'NOT_FOUND',
  SERVER_ERROR: 'SERVER_ERROR'
};

export const FILTER_OPTIONS = {
  ALL: 'all',
  COMPLETED: 'completed',
  INCOMPLETE: 'incomplete'
};

// Default values for task queries
export const DEFAULT_QUERY_PARAMS = {
  limit: 100,
  offset: 0,
  sort: SORT_OPTIONS.CREATED_AT,
  order: SORT_ORDER.DESC
};

// UI Messages
export const MESSAGES = {
  LOADING: 'Loading tasks...',
  EMPTY_LIST: 'No tasks found. Create your first task!',
  ERROR_GENERIC: 'Something went wrong. Please try again.',
  ERROR_NETWORK: 'Network error. Please check your connection.',
  SUCCESS_CREATE: 'Task created successfully!',
  SUCCESS_UPDATE: 'Task updated successfully!',
  SUCCESS_DELETE: 'Task deleted successfully!',
  CONFIRM_DELETE: 'Are you sure you want to delete this task?'
};

// Form validation rules
export const VALIDATION_RULES = {
  TITLE: {
    required: true,
    minLength: 1,
    maxLength: 200
  },
  DESCRIPTION: {
    required: false,
    maxLength: 1000
  }
};