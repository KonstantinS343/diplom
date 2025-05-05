<template>
  <div class="marked-text-container">
    <div class="text-content">
      <span v-for="(part, index) in processedText" :key="index" :class="getPartClass(part)">
        {{ part.text }}
        <v-tooltip v-if="part.type === 'replace'" location="top">
          <template v-slot:activator="{ props }">
            <span v-bind="props" class="tooltip-trigger">?</span>
          </template>
          <span>Предлагаемый вариант: {{ part.new }}</span>
        </v-tooltip>
      </span>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue';

const props = defineProps({
  text: {
    type: String,
    required: true
  }
});

const processedText = computed(() => {
  const parts = [];
  let currentText = props.text;
  
  // Регулярные выражения для поиска тегов
  const insRegex = /<ins>(.*?)<\/ins>/g;
  const delRegex = /<del>(.*?)<\/del>/g;
  const replaceRegex = /<replace new='(.*?)'>(.*?)<\/replace>/g;
  
  // Обработка тегов replace
  currentText = currentText.replace(replaceRegex, (match, newText, oldText) => {
    parts.push({ type: 'replace', text: oldText, new: newText });
    return `__REPLACE_${parts.length - 1}__`;
  });
  
  // Обработка тегов ins
  currentText = currentText.replace(insRegex, (match, text) => {
    parts.push({ type: 'ins', text });
    return `__INS_${parts.length - 1}__`;
  });
  
  // Обработка тегов del
  currentText = currentText.replace(delRegex, (match, text) => {
    parts.push({ type: 'del', text });
    return `__DEL_${parts.length - 1}__`;
  });
  
  // Добавляем обычный текст
  const textParts = currentText.split(/__(?:REPLACE|INS|DEL)_\d+__/);
  const result = [];
  
  textParts.forEach((text, index) => {
    if (text) {
      result.push({ type: 'normal', text });
    }
    if (index < textParts.length - 1) {
      const partIndex = currentText.match(/__(?:REPLACE|INS|DEL)_(\d+)__/g)[index].match(/\d+/)[0];
      result.push(parts[partIndex]);
    }
  });
  
  return result;
});

const getPartClass = (part) => {
  switch (part.type) {
    case 'ins':
      return 'marked-ins';
    case 'del':
      return 'marked-del';
    case 'replace':
      return 'marked-replace';
    default:
      return '';
  }
};
</script>

<style scoped>
.marked-text-container {
  position: relative;
  width: 100%;
  height: 100%;
}

.text-content {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  white-space: pre-wrap;
  line-height: 1.5;
  pointer-events: none;
  z-index: 1;
}

.marked-ins {
  background-color: rgba(76, 175, 80, 0.2);
  padding: 2px 4px;
  border-radius: 2px;
  pointer-events: auto;
  display: inline;
}

.marked-del {
  background-color: rgba(244, 67, 54, 0.2);
  padding: 2px 4px;
  border-radius: 2px;
  text-decoration: line-through;
  pointer-events: auto;
  display: inline;
}

.marked-replace {
  background-color: rgba(255, 235, 59, 0.2);
  padding: 2px 4px;
  border-radius: 2px;
  position: relative;
  display: inline;
  pointer-events: auto;
}

.tooltip-trigger {
  font-size: 0.8em;
  margin-left: 2px;
  color: #666;
  cursor: help;
  pointer-events: auto;
  display: inline-block;
}

:deep(.v-tooltip__content) {
  background-color: rgba(0, 0, 0, 0.8) !important;
  padding: 8px 12px !important;
  border-radius: 4px !important;
  font-size: 0.9em !important;
}
</style> 