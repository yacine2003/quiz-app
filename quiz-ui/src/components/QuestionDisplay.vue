<script setup>
import { defineProps, defineEmits } from 'vue';

const props = defineProps({
  question: {
    type: Object,
    required: true
  }
});

const emit = defineEmits(['answer-clicked']);
</script>

<template>
  <div class="question-display">
    <h2>{{ question.text }}</h2>
    
    <img v-if="question.image" :src="question.image" alt="Question image" class="question-image" />
    
    <div class="answers">
      <button 
        v-for="answer in question.possibleAnswers" 
        :key="answer.text"
        @click="emit('answer-clicked', answer)"
        class="btn btn-outline-primary answer-btn"
      >
        {{ answer.text }}
      </button>
    </div>
  </div>
</template>

<style scoped>
.question-display {
  max-width: 800px;
  margin: 20px auto;
}

.question-image {
  max-width: 100%;
  height: auto;
  margin: 20px 0;
  border-radius: 8px;
}

.answers {
  display: flex;
  flex-direction: column;
  gap: 10px;
  margin-top: 20px;
}

.answer-btn {
  padding: 15px;
  text-align: left;
  width: 100%;
}
</style>
