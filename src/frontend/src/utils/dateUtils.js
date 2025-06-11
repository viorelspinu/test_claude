import { format, parseISO, isValid, isBefore, isAfter, startOfDay } from 'date-fns'

/**
 * Format a date string for display
 * @param {string|Date} date - Date to format
 * @param {string} formatString - Format string (default: 'MMM dd, yyyy')
 * @returns {string} Formatted date string
 */
export const formatDate = (date, formatString = 'MMM dd, yyyy') => {
  if (!date) return ''
  
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    if (!isValid(dateObj)) return ''
    return format(dateObj, formatString)
  } catch (error) {
    console.error('Error formatting date:', error)
    return ''
  }
}

/**
 * Format a datetime string for display
 * @param {string|Date} datetime - Datetime to format
 * @returns {string} Formatted datetime string
 */
export const formatDateTime = (datetime) => {
  return formatDate(datetime, 'MMM dd, yyyy at h:mm a')
}

/**
 * Check if a date is overdue (before today)
 * @param {string|Date} date - Date to check
 * @returns {boolean} True if overdue
 */
export const isOverdue = (date) => {
  if (!date) return false
  
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    if (!isValid(dateObj)) return false
    return isBefore(startOfDay(dateObj), startOfDay(new Date()))
  } catch (error) {
    console.error('Error checking overdue status:', error)
    return false
  }
}

/**
 * Check if a date is in the future
 * @param {string|Date} date - Date to check
 * @returns {boolean} True if in future
 */
export const isFutureDate = (date) => {
  if (!date) return false
  
  try {
    const dateObj = typeof date === 'string' ? parseISO(date) : date
    if (!isValid(dateObj)) return false
    return isAfter(startOfDay(dateObj), startOfDay(new Date()))
  } catch (error) {
    console.error('Error checking future date:', error)
    return false
  }
}

/**
 * Get today's date in YYYY-MM-DD format for input fields
 * @returns {string} Today's date in YYYY-MM-DD format
 */
export const getTodayString = () => {
  return format(new Date(), 'yyyy-MM-dd')
}

export default {
  formatDate,
  formatDateTime,
  isOverdue,
  isFutureDate,
  getTodayString,
}