import { ref } from 'vue';

const snackbar = ref({
  show: false,
  text: '',
  color: 'error',
  timeout: 3000
});

export function useSnackbar() {
  const showError = (message) => {
    snackbar.value = {
      show: true,
      text: message,
      color: 'error',
      timeout: 3000
    };
  };

  const showSuccess = (message) => {
    snackbar.value = {
      show: true,
      text: message,
      color: 'success',
      timeout: 3000
    };
  };

  return {
    snackbar,
    showError,
    showSuccess
  };
} 