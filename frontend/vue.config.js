module.exports = {
  transpileDependencies: ['vue-cli-plugin'],
  devServer: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000', // URL do backend Django
        changeOrigin: true,
        pathRewrite: { '^/api': '' }, // Opcional: remove '/api' ao encaminhar para o backend
      },
    },
  },
};
