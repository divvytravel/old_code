define(["jquery"],function($) {

	// Эта штука нужна, чтобы в будущем делать запросы за данными, которых не оказалось в кеше
	// Типа если есть данные в DataProvider - отдаем их, нет - запрашиваем, сохраняем себе и отдаем

	var DataProvider = function(startData) {
		this.data = $.extend({},startData);
		this.prepare();
	}

	DataProvider.prototype.prepare = function() {
		// Предварительная обработка данных
		
	}

	DataProvider.prototype.get = function() {
		var out = this.data;
		for (var i = 0; i < arguments.length; i++) {
			if (typeof out == "object")
				out = out[arguments[i]];
			else return null;
		}
		return out;
	}

	return DataProvider;
});
