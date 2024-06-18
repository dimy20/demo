//import { defineConfig } from 'vite';
//export default defineConfig({
//  server: {
//    proxy: {
//      '/api': {
//        target: 'http://vigilant-ai-api:80',
//        changeOrigin: true,
//        secure: false,
//      },
//    },
//  },
//})
//import { defineConfig } from 'vite';

export default defineConfig({
  server: {
    proxy: {
      //'/api': {
      //  target: 'http://vigilant-ai-api:80',
      //  changeOrigin: true,
      //  secure: false,
      //},
    //  '/stream': {
    //    target: 'ws://vigilant-ai-api:80',
    //    ws: true,
    //    changeOrigin: true,
    //    secure: false,
    //  },
    },
  },
});
