gulp        = (require 'gulp-help')(require 'gulp')
plug        = (require 'gulp-load-plugins')()
path        = require 'path'
env         = require './.gulp/env'
conf        = require './.gulp/conf'

gulp.task 'default', 'Run build or watch (dev environment).',
    [if env.dev then 'watch' else 'build']

gulp.task 'watch', 'Watch sources changes.', ['build'], ->
    gulp.watch conf.scripts, ['scripts']
    gulp.watch conf.data, ['data']

gulp.task 'build', 'Build node application.', ['scripts', 'data']

gulp.task 'scripts', 'Compile ES2015 scripts to ES5.', ->
    gulp.src conf.scripts
        .pipe plug.plumber()
        .pipe plug.changed conf.dest
        .pipe plug.jshint '.jshintrc'
        .pipe plug.jshint.reporter 'jshint-stylish'
        .pipe plug.sourcemaps.init loadMaps: true
            .pipe plug.babel optional: ['runtime']
            .pipe plug.uglify()
        .pipe plug.sourcemaps.write '.', sourceRoot: path.resolve(conf.srcs)
        .pipe gulp.dest conf.dest
        .pipe plug.if(env.notify, plug.notify
            onLast: true
            message: -> 'JavaScript files compiled')

gulp.task 'data', 'Copy data directory.', ->
    gulp.src conf.data
        .pipe gulp.dest "#{conf.dest}/data"

gulp.task 'clean', 'Clean dist directory.', ->
    gulp.src "#{conf.dest}/*", read: false
        .pipe plug.rimraf()

gulp.task 'rebuild', 'Rebuild.', ->
    (require 'run-sequence') 'clean', 'build'

gulp.task 'env', 'Display gulp environment variables.', ->
    console.log JSON.stringify(env, null, 4)
