<template>
  <div class="chat-container">
    <div class="chat-header">
      <h2>通义千问 AI 助手</h2>
      <span class="status" :class="{ online: isOnline }">
        {{ isOnline ? '在线' : '离线' }}
      </span>
    </div>

    <div class="chat-messages" ref="messagesContainer">
      <div
        v-for="(message, index) in messages"
        :key="index"
        class="message"
        :class="message.role"
      >
        <div class="avatar">
          {{ message.role === 'user' ? '👤' : '🤖' }}
        </div>
        <div class="content">
          <p>{{ message.content }}</p>
        </div>
      </div>
      <div v-if="loading" class="message loading">
        <div class="avatar">🤖</div>
        <div class="content">
          <div class="typing">
            <span></span>
            <span></span>
            <span></span>
          </div>
        </div>
      </div>
    </div>

    <div class="chat-input">
      <textarea
        v-model="inputMessage"
        @keydown.enter.exact.prevent="sendMessage"
        placeholder="输入您的问题..."
        rows="2"
      ></textarea>
      <button @click="sendMessage" :disabled="!inputMessage.trim() || loading">
        发送
      </button>
    </div>
  </div>
</template>

<script setup>import { ref, onMounted, nextTick } from 'vue';
import { generateChat } from '@/utils/qianwen';
const messages = ref([
 { role: 'model', content: '您好！我是通义千问 AI 助手。有什么我可以帮助您的吗？' }
]);
const inputMessage = ref('');
const loading = ref(false);
const isOnline = ref(true);
const messagesContainer = ref(null);
async function sendMessage() {
 if (!inputMessage.value.trim() || loading.value)
 return;
 const userMessage = inputMessage.value.trim();
 messages.value.push({ role: 'user', content: userMessage });
 inputMessage.value = '';
 loading.value = true;
 await scrollToBottom();
 try {
 const response = await generateChat(messages.value);
 messages.value.push({ role: 'model', content: response });
 }
 catch (error) {
 messages.value.push({
 role: 'model',
 content: `抱歉，发生错误：${error.message}`
 });
 isOnline.value = false;
 }
 finally {
 loading.value = false;
 await scrollToBottom();
 }
}
async function scrollToBottom() {
 await nextTick();
 if (messagesContainer.value) {
 messagesContainer.value.scrollTop = messagesContainer.value.scrollHeight;
 }
}
onMounted(() => {
 scrollToBottom();
});
</script>

<style scoped lang="scss">
.chat-container {
  display: flex;
  flex-direction: column;
  height: 500px;
  border: 1px solid #e0e0e0;
  border-radius: 12px;
  overflow: hidden;
  background: #fff;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.chat-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 16px 20px;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;

  h2 {
    margin: 0;
    font-size: 18px;
    font-weight: 600;
  }

  .status {
    font-size: 12px;
    padding: 4px 12px;
    border-radius: 20px;
    background: rgba(255, 255, 255, 0.2);

    &.online {
      background: rgba(76, 175, 80, 0.8);
    }
  }
}

.chat-messages {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
  background: #f8f9fa;

  .message {
    display: flex;
    margin-bottom: 16px;
    animation: fadeIn 0.3s ease;

    &.user {
      justify-content: flex-end;

      .content {
        background: #667eea;
        color: white;
        border-radius: 16px 16px 4px 16px;
      }
    }

    &.model {
      justify-content: flex-start;

      .content {
        background: white;
        color: #333;
        border-radius: 16px 16px 16px 4px;
        box-shadow: 0 1px 3px rgba(0, 0, 0, 0.05);
      }
    }

    &.loading {
      .typing {
        display: flex;
        gap: 4px;
        padding: 8px 12px;

        span {
          width: 8px;
          height: 8px;
          border-radius: 50%;
          background: #ccc;
          animation: typing 1.4s infinite ease-in-out;

          &:nth-child(2) {
            animation-delay: 0.2s;
          }

          &:nth-child(3) {
            animation-delay: 0.4s;
          }
        }
      }
    }

    .avatar {
      width: 36px;
      height: 36px;
      border-radius: 50%;
      display: flex;
      align-items: center;
      justify-content: center;
      font-size: 18px;
      flex-shrink: 0;
      margin: 0 8px;
    }

    .content {
      max-width: 70%;
      padding: 12px 16px;

      p {
        margin: 0;
        line-height: 1.6;
        word-break: break-word;
      }
    }
  }
}

.chat-input {
  display: flex;
  gap: 12px;
  padding: 16px;
  border-top: 1px solid #e0e0e0;
  background: white;

  textarea {
    flex: 1;
    padding: 12px 16px;
    border: 1px solid #e0e0e0;
    border-radius: 8px;
    resize: none;
    font-size: 14px;
    line-height: 1.4;
    outline: none;
    transition: border-color 0.2s;

    &:focus {
      border-color: #667eea;
    }

    &::placeholder {
      color: #999;
    }
  }

  button {
    padding: 12px 24px;
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: white;
    border: none;
    border-radius: 8px;
    font-size: 14px;
    font-weight: 500;
    cursor: pointer;
    transition: opacity 0.2s;

    &:hover:not(:disabled) {
      opacity: 0.9;
    }

    &:disabled {
      opacity: 0.5;
      cursor: not-allowed;
    }
  }
}

@keyframes fadeIn {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes typing {
  0%, 80%, 100% {
    transform: scale(0.6);
    opacity: 0.5;
  }
  40% {
    transform: scale(1);
    opacity: 1;
  }
}
</style>
