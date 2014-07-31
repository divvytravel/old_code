module.exports = function(grunt) {

    // Задачи
    grunt.initConfig({

        sass: {
            dist: {
                options: {
                    // style: 'compressed'
                    style: 'expanded'
                },
                files: {
                    'css/theme.css': 'styles/theme.scss'
                }
            }
        },
        watch: {
          sass: {
            options: {
              livereload: false
            },
            files: ['styles/**/*.scss'],
            tasks: ['sass'],
          }
        }

    });

    // Загрузка плагинов, установленных с помощью npm install
    grunt.loadNpmTasks('grunt-contrib-sass');
    grunt.loadNpmTasks('grunt-contrib-watch');

    // Задача по умолчанию
    grunt.registerTask('default', ['watch']);
};
