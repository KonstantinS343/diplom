<template>
  <div class="about">
    <div class="content-wrapper">
      <div class="page-header">
        <h1 class="text-h4 mb-2">О платформе</h1>
        <p class="text-body-1 text-medium-emphasis">
          Узнайте больше о возможностях и преимуществах нашей платформы
        </p>
      </div>

      <div class="hero-section">
        <div class="hero-stats">
          <div class="stat-item">
            <span class="stat-value">98%</span>
            <span class="stat-label">Точность</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">12+</span>
            <span class="stat-label">Языков</span>
          </div>
          <div class="stat-item">
            <span class="stat-value">24/7</span>
            <span class="stat-label">Доступность</span>
          </div>
        </div>
      </div>

      <div class="features-section">
        <h2 class="text-h4 mb-6">Возможности платформы</h2>
        <div class="features-grid">
          <div class="feature-card">
            <v-icon icon="mdi-file-document" size="32" color="grey-darken-2"></v-icon>
            <h3 class="text-h6 mt-4">Перевод документов</h3>
            <p class="text-body-2">Поддержка форматов DOC, DOCX, XLSX, PPTX с сохранением форматирования</p>
          </div>
          <div class="feature-card">
            <v-icon icon="mdi-brain" size="32" color="grey-darken-2"></v-icon>
            <h3 class="text-h6 mt-4">ИИ технологии</h3>
            <p class="text-body-2">Использование передовых моделей машинного обучения для точного перевода</p>
          </div>
          <div class="feature-card">
            <v-icon icon="mdi-account-group" size="32" color="grey-darken-2"></v-icon>
            <h3 class="text-h6 mt-4">Сообщество</h3>
            <p class="text-body-2">Участвуйте в улучшении качества переводов и помогайте другим</p>
          </div>
        </div>
      </div>

      <div class="cta-section">
        <h2 class="text-h4 mb-4">Готовы начать?</h2>
        <p class="text-body-1 text-medium-emphasis mb-6">
          Присоединяйтесь к сообществу и получите доступ ко всем возможностям платформы
        </p>
        <div class="cta-buttons">
          <v-btn
            color="grey-darken-2"
            size="large"
            to="/"
          >
            Начать перевод
          </v-btn>
          <v-btn
            color="grey-darken-2"
            variant="outlined"
            size="large"
            to="/learning"
          >
            Узнать больше
          </v-btn>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
// Нет необходимости в дополнительной логике для страницы о платформе
</script>

<style scoped>
.about {
  padding: 24px;
  max-width: 1800px;
  margin: 0 auto;
}

.content-wrapper {
  width: 100%;
}

.page-header {
  text-align: center;
  margin-bottom: 32px;
}

.hero-section {
  text-align: center;
  padding: 32px 0;
  margin-bottom: 48px;
}

.hero-stats {
  display: flex;
  justify-content: center;
  gap: 48px;
  margin-top: 32px;
}

.stat-item {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 8px;
}

.stat-value {
  font-size: 2rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.87);
}

.stat-label {
  font-size: 1rem;
  color: rgba(0, 0, 0, 0.6);
}

.features-section {
  margin-bottom: 48px;
}

.features-section h2 {
  text-align: center;
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.features-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 32px;
}

.feature-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.feature-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.feature-card h3 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.feature-card p {
  color: rgba(0, 0, 0, 0.6);
  margin-top: 8px;
}


.steps-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 24px;
  margin-top: 32px;
}

.step-card {
  background: white;
  padding: 32px;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  text-align: center;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  border: 1px solid rgba(0, 0, 0, 0.12);
  position: relative;
}

.step-card:hover {
  transform: translateY(-4px);
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.15);
}

.step-number {
  width: 40px;
  height: 40px;
  background: rgba(0, 0, 0, 0.05);
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.2rem;
  font-weight: 500;
  color: rgba(0, 0, 0, 0.87);
  margin: 0 auto;
}

.step-card h3 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.step-card p {
  color: rgba(0, 0, 0, 0.6);
  margin-top: 8px;
}

.cta-section {
  text-align: center;
  padding: 64px 0;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  border: 1px solid rgba(0, 0, 0, 0.12);
}

.cta-section h2 {
  color: rgba(0, 0, 0, 0.87);
  font-weight: 500;
}

.cta-buttons {
  display: flex;
  justify-content: center;
  gap: 16px;
}
</style> 