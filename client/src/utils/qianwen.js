const API_KEY = import.meta.env.VITE_QIANWEN_API_KEY;
const API_URL = 'https://dashscope.aliyuncs.com/api/text-generation/v1';
export async function generateText(prompt) {
 try {
 const response = await fetch(API_URL, {
 method: 'POST',
 headers: {
 'Content-Type': 'application/json',
 'Authorization': `Bearer ${API_KEY}`
 },
 body: JSON.stringify({
 model: 'qwen-turbo',
 input: {
 messages: [
 {
 role: 'user',
 content: prompt
 }
 ]
 },
 parameters: {
 result_format: 'message'
 }
 })
 });
 if (!response.ok) {
 const errorData = await response.json().catch(() => ({}));
 throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
 }
 const data = await response.json();
 if (data.output && data.output.choices && data.output.choices.length > 0) {
 return data.output.choices[0].message.content;
 }
 throw new Error('未能获取到响应内容');
 }
 catch (error) {
 console.error('Qianwen API Error:', error);
 throw new Error(error.message || 'AI 请求失败');
 }
}
export async function generateChat(messages) {
 try {
 const formattedMessages = messages.map(msg => ({
 role: msg.role,
 content: msg.content
 }));
 const response = await fetch(API_URL, {
 method: 'POST',
 headers: {
 'Content-Type': 'application/json',
 'Authorization': `Bearer ${API_KEY}`
 },
 body: JSON.stringify({
 model: 'qwen-turbo',
 input: {
 messages: formattedMessages
 },
 parameters: {
 result_format: 'message'
 }
 })
 });
 if (!response.ok) {
 const errorData = await response.json().catch(() => ({}));
 throw new Error(errorData.message || `HTTP error! status: ${response.status}`);
 }
 const data = await response.json();
 if (data.output && data.output.choices && data.output.choices.length > 0) {
 return data.output.choices[0].message.content;
 }
 throw new Error('未能获取到响应内容');
 }
 catch (error) {
 console.error('Qianwen Chat Error:', error);
 throw new Error(error.message || 'AI 聊天请求失败');
 }
}
