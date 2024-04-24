(self["webpackChunklibro_lab"] = self["webpackChunklibro_lab"] || []).push([[9060],{

/***/ 49059:
/***/ (function(module) {

function webpackEmptyContext(req) {
	var e = new Error("Cannot find module '" + req + "'");
	e.code = 'MODULE_NOT_FOUND';
	throw e;
}
webpackEmptyContext.keys = function() { return []; };
webpackEmptyContext.resolve = webpackEmptyContext;
webpackEmptyContext.id = 49059;
module.exports = webpackEmptyContext;

/***/ }),

/***/ 94867:
/***/ (function(__unused_webpack_module, __webpack_exports__, __webpack_require__) {

"use strict";
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  "default": function() { return /* binding */ execution; }
});

// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/module/mana-module.js
var mana_module = __webpack_require__(17354);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/decorator.js
var decorator = __webpack_require__(64424);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-protocol.js
var view_protocol = __webpack_require__(45573);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-app/es/view/header/header-view.js + 1 modules
var header_view = __webpack_require__(87845);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/components/index.js + 6 modules
var components = __webpack_require__(90191);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-app/es/index.js + 39 modules
var es = __webpack_require__(55831);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-lab/es/index.js + 110 modules
var libro_lab_es = __webpack_require__(52475);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-jupyter/es/index.js + 381 modules
var libro_jupyter_es = __webpack_require__(24159);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/regeneratorRuntime.js
var regeneratorRuntime = __webpack_require__(15009);
var regeneratorRuntime_default = /*#__PURE__*/__webpack_require__.n(regeneratorRuntime);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/asyncToGenerator.js
var asyncToGenerator = __webpack_require__(99289);
var asyncToGenerator_default = /*#__PURE__*/__webpack_require__.n(asyncToGenerator);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/initializerDefineProperty.js
var initializerDefineProperty = __webpack_require__(19911);
var initializerDefineProperty_default = /*#__PURE__*/__webpack_require__.n(initializerDefineProperty);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/classCallCheck.js
var classCallCheck = __webpack_require__(12444);
var classCallCheck_default = /*#__PURE__*/__webpack_require__.n(classCallCheck);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/createClass.js
var createClass = __webpack_require__(72004);
var createClass_default = /*#__PURE__*/__webpack_require__.n(createClass);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/applyDecoratedDescriptor.js
var applyDecoratedDescriptor = __webpack_require__(65371);
var applyDecoratedDescriptor_default = /*#__PURE__*/__webpack_require__.n(applyDecoratedDescriptor);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/initializerWarningHelper.js
var initializerWarningHelper = __webpack_require__(45966);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/configuration/configuration-service.js
var configuration_service = __webpack_require__(52243);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/slot-view-manager.js
var slot_view_manager = __webpack_require__(94104);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/application/application.js
var application = __webpack_require__(15910);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-manager.js
var view_manager = __webpack_require__(44659);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-syringe/es/index.js + 15 modules
var mana_syringe_es = __webpack_require__(49383);
;// CONCATENATED MODULE: ./src/pages/execution/app.ts







var _dec, _dec2, _dec3, _dec4, _dec5, _dec6, _dec7, _class, _class2, _descriptor, _descriptor2, _descriptor3, _descriptor4, _descriptor5, _descriptor6;





var LibroApp = (_dec = (0,mana_syringe_es/* singleton */.ri)({
  contrib: application/* ApplicationContribution */.rS
}), _dec2 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerConnection */.Ner), _dec3 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerManager */.ErZ), _dec4 = (0,mana_syringe_es/* inject */.f3)(view_manager/* ViewManager */.v), _dec5 = (0,mana_syringe_es/* inject */.f3)(slot_view_manager/* SlotViewManager */.I), _dec6 = (0,mana_syringe_es/* inject */.f3)(configuration_service/* ConfigurationService */.e), _dec7 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* FileCommandContribution */.uq5), _dec(_class = (_class2 = /*#__PURE__*/function () {
  function LibroApp() {
    classCallCheck_default()(this, LibroApp);
    initializerDefineProperty_default()(this, "serverConnection", _descriptor, this);
    initializerDefineProperty_default()(this, "serverManager", _descriptor2, this);
    initializerDefineProperty_default()(this, "viewManager", _descriptor3, this);
    initializerDefineProperty_default()(this, "slotViewManager", _descriptor4, this);
    initializerDefineProperty_default()(this, "configurationService", _descriptor5, this);
    initializerDefineProperty_default()(this, "fileCommandContribution", _descriptor6, this);
  }
  createClass_default()(LibroApp, [{
    key: "onStart",
    value: function () {
      var _onStart = asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee() {
        var baseUrl, el, pageConfig;
        return regeneratorRuntime_default()().wrap(function _callee$(_context) {
          while (1) switch (_context.prev = _context.next) {
            case 0:
              document.title = "libro execution";
              this.configurationService.set(libro_jupyter_es/* LibroJupyterConfiguration */.WLy.AllowDownload, true);
              this.configurationService.set(libro_jupyter_es/* LibroJupyterConfiguration */.WLy.AllowUpload, true);
              this.fileCommandContribution.allowUpload = true;
              this.fileCommandContribution.allowDownload = true;
              baseUrl = libro_jupyter_es/* PageConfig */.Pzp.getOption('baseUrl');
              el = document.getElementById('jupyter-config-data');
              if (el) {
                pageConfig = JSON.parse(el.textContent || '');
                baseUrl = pageConfig['baseUrl'];
                if (baseUrl && baseUrl.startsWith('/')) {
                  baseUrl = window.location.origin + baseUrl;
                }
              }
              this.serverConnection.updateSettings({
                baseUrl: baseUrl,
                wsUrl: baseUrl.replace(/^http(s)?/, 'ws$1')
              });
              this.serverManager.launch();
            case 10:
            case "end":
              return _context.stop();
          }
        }, _callee, this);
      }));
      function onStart() {
        return _onStart.apply(this, arguments);
      }
      return onStart;
    }()
  }]);
  return LibroApp;
}(), (_descriptor = applyDecoratedDescriptor_default()(_class2.prototype, "serverConnection", [_dec2], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor2 = applyDecoratedDescriptor_default()(_class2.prototype, "serverManager", [_dec3], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor3 = applyDecoratedDescriptor_default()(_class2.prototype, "viewManager", [_dec4], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor4 = applyDecoratedDescriptor_default()(_class2.prototype, "slotViewManager", [_dec5], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor5 = applyDecoratedDescriptor_default()(_class2.prototype, "configurationService", [_dec6], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor6 = applyDecoratedDescriptor_default()(_class2.prototype, "fileCommandContribution", [_dec7], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
})), _class2)) || _class);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/assertThisInitialized.js
var assertThisInitialized = __webpack_require__(25098);
var assertThisInitialized_default = /*#__PURE__*/__webpack_require__.n(assertThisInitialized);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/inherits.js
var inherits = __webpack_require__(31996);
var inherits_default = /*#__PURE__*/__webpack_require__.n(inherits);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/createSuper.js
var createSuper = __webpack_require__(26037);
var createSuper_default = /*#__PURE__*/__webpack_require__.n(createSuper);
// EXTERNAL MODULE: ./node_modules/@umijs/preset-umi/node_modules/react/index.js
var react = __webpack_require__(62435);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-observable/es/index.js + 12 modules
var mana_observable_es = __webpack_require__(94725);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/view-render.js
var view_render = __webpack_require__(41814);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-common/es/uri.js + 4 modules
var uri = __webpack_require__(26587);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-common/es/promise-util.js
var promise_util = __webpack_require__(33422);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/default-view.js + 1 modules
var default_view = __webpack_require__(58304);
// EXTERNAL MODULE: ./node_modules/query-string/index.js + 4 modules
var query_string = __webpack_require__(94785);
// EXTERNAL MODULE: ./node_modules/antd/es/button/index.js + 9 modules
var es_button = __webpack_require__(14726);
// EXTERNAL MODULE: ./node_modules/antd/es/spin/index.js + 2 modules
var spin = __webpack_require__(75081);
// EXTERNAL MODULE: ./node_modules/@rjsf/antd/lib/index.js + 102 modules
var lib = __webpack_require__(65961);
// EXTERNAL MODULE: ./node_modules/@rjsf/validator-ajv8/lib/index.js + 6 modules
var validator_ajv8_lib = __webpack_require__(74717);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-react/es/index.js + 77 modules
var mana_react_es = __webpack_require__(47185);
;// CONCATENATED MODULE: ./src/pages/execution/index.less
// extracted by mini-css-extract-plugin

// EXTERNAL MODULE: ./node_modules/@umijs/preset-umi/node_modules/react/jsx-runtime.js
var jsx_runtime = __webpack_require__(86074);
;// CONCATENATED MODULE: ./src/pages/execution/execution-view.tsx










var execution_view_dec, execution_view_dec2, execution_view_dec3, execution_view_dec4, execution_view_dec5, execution_view_dec6, execution_view_dec7, _dec8, _dec9, _dec10, _dec11, _dec12, execution_view_class, execution_view_class2, execution_view_descriptor, execution_view_descriptor2, execution_view_descriptor3, execution_view_descriptor4, execution_view_descriptor5, execution_view_descriptor6, _descriptor7, _descriptor8, _descriptor9, _descriptor10;












function SubmitButton(props) {
  return /*#__PURE__*/(0,jsx_runtime.jsx)(es_button/* default */.ZP, {
    type: "primary",
    htmlType: "submit",
    children: "Submit"
  });
}
var LibroExecutionComponent = /*#__PURE__*/(0,react.forwardRef)(function (props, ref) {
  var formRef = (0,react.useRef)(null);
  var instance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var queryParams = query_string/* default */.Z.parse(window.location.search);
  var filePath = queryParams['path'];
  var libroView = (0,mana_observable_es/* useObserve */.Re)(instance.libroView);
  (0,react.useEffect)(function () {
    if (filePath && typeof filePath === 'string') {
      instance.path = filePath;
    }
  }, [filePath]);
  (0,react.useEffect)(function () {
    if (libroView !== null && libroView !== void 0 && libroView.model.metadata) {
      var metadata = libroView === null || libroView === void 0 ? void 0 : libroView.model.metadata;
      if (metadata && metadata['args']) {
        instance.schema = metadata['args'];
        return;
      }
    }
  }, [libroView === null || libroView === void 0 ? void 0 : libroView.model.isInitialized]);
  var onSub = function onSub(data) {
    var formData = data.formData;
    instance.execute(formData);
  };
  if (!queryParams['path']) {
    return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      children: "\u9700\u8981\u6307\u5B9A\u8981\u6267\u884C\u7684\u6587\u4EF6"
    });
  }
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-execution-container",
    ref: ref,
    children: /*#__PURE__*/(0,jsx_runtime.jsxs)(mana_react_es/* BoxPanel */.jN, {
      className: "libro-execution-container-wrapper",
      direction: "left-to-right",
      children: [/*#__PURE__*/(0,jsx_runtime.jsxs)(mana_react_es/* BoxPanel */.jN.Pane, {
        className: "libro-execution-container-left",
        children: [instance.executing && /*#__PURE__*/(0,jsx_runtime.jsx)(spin/* default */.Z, {
          spinning: instance.executing,
          tip: "".concat(instance.currentIndex, "/").concat(instance.count),
          children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
            style: {
              height: 200,
              width: '100%'
            }
          })
        }), !instance.executing && instance.resultView && /*#__PURE__*/(0,jsx_runtime.jsx)(view_render/* ViewRender */.o, {
          view: instance.resultView
        })]
      }), /*#__PURE__*/(0,jsx_runtime.jsx)(mana_react_es/* BoxPanel */.jN.Pane, {
        className: "libro-execution-container-right",
        flex: 1,
        children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
          children: instance.schema && /*#__PURE__*/(0,jsx_runtime.jsx)(lib/* default */.ZP, {
            ref: formRef,
            schema: instance.schema,
            validator: validator_ajv8_lib/* default */.ZP,
            onSubmit: onSub,
            templates: {
              ButtonTemplates: {
                SubmitButton: SubmitButton
              }
            }
          })
        })
      })]
    })
  });
});
var LibroExecutionView = (execution_view_dec = (0,mana_syringe_es/* singleton */.ri)(), execution_view_dec2 = (0,decorator/* view */.ei)('libro-execution-view'), execution_view_dec3 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* ServerConnection */.Ner), execution_view_dec4 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* LibroFileService */.tL0), execution_view_dec5 = (0,mana_syringe_es/* inject */.f3)(libro_jupyter_es/* LibroService */.W$M), execution_view_dec6 = (0,mana_observable_es/* prop */.vg)(), execution_view_dec7 = (0,mana_observable_es/* prop */.vg)(), _dec8 = (0,mana_observable_es/* prop */.vg)(), _dec9 = (0,mana_observable_es/* prop */.vg)(), _dec10 = (0,mana_observable_es/* prop */.vg)(), _dec11 = (0,mana_observable_es/* prop */.vg)(), _dec12 = (0,mana_observable_es/* prop */.vg)(), execution_view_dec(execution_view_class = execution_view_dec2(execution_view_class = (execution_view_class2 = /*#__PURE__*/function (_BaseView) {
  inherits_default()(LibroExecutionView, _BaseView);
  var _super = createSuper_default()(LibroExecutionView);
  function LibroExecutionView() {
    var _this;
    classCallCheck_default()(this, LibroExecutionView);
    for (var _len = arguments.length, _args = new Array(_len), _key = 0; _key < _len; _key++) {
      _args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(_args));
    initializerDefineProperty_default()(_this, "serverConnection", execution_view_descriptor, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "fileService", execution_view_descriptor2, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "libroService", execution_view_descriptor3, assertThisInitialized_default()(_this));
    _this.view = LibroExecutionComponent;
    initializerDefineProperty_default()(_this, "libroView", execution_view_descriptor4, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "schema", execution_view_descriptor5, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "resultView", execution_view_descriptor6, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "executionId", _descriptor7, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "executing", _descriptor8, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "count", _descriptor9, assertThisInitialized_default()(_this));
    initializerDefineProperty_default()(_this, "currentIndex", _descriptor10, assertThisInitialized_default()(_this));
    _this._path = void 0;
    _this.update = /*#__PURE__*/asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee() {
      return regeneratorRuntime_default()().wrap(function _callee$(_context) {
        while (1) switch (_context.prev = _context.next) {
          case 0:
            _this.schema = undefined;
            if (_this.path) {
              _context.next = 3;
              break;
            }
            return _context.abrupt("return");
          case 3:
            document.title = "execution: ".concat(_this.path);
            _context.next = 6;
            return _this.libroService.getOrCreateView({
              resource: _this.path
            });
          case 6:
            _this.libroView = _context.sent;
            _this.updateExecutionResult();
          case 8:
          case "end":
            return _context.stop();
        }
      }, _callee);
    }));
    _this.updateExecutionResult = /*#__PURE__*/asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee2() {
      var file, baseName, resultUri, resultPath, tryRead;
      return regeneratorRuntime_default()().wrap(function _callee2$(_context2) {
        while (1) switch (_context2.prev = _context2.next) {
          case 0:
            _context2.prev = 0;
            file = new uri/* URI */.o(_this.path);
            baseName = file.path.base;
            resultUri = uri/* URI */.o.resolve(file, "../execution/".concat(baseName));
            resultPath = resultUri.path.toString();
            _context2.next = 7;
            return _this.fileService.read(resultPath);
          case 7:
            tryRead = _context2.sent;
            if (!tryRead) {
              _context2.next = 12;
              break;
            }
            _context2.next = 11;
            return _this.libroService.getOrCreateView({
              resource: resultPath
            });
          case 11:
            _this.resultView = _context2.sent;
          case 12:
            _context2.next = 16;
            break;
          case 14:
            _context2.prev = 14;
            _context2.t0 = _context2["catch"](0);
          case 16:
          case "end":
            return _context2.stop();
        }
      }, _callee2, null, [[0, 14]]);
    }));
    _this.execute = /*#__PURE__*/function () {
      var _ref3 = asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee3(args) {
        var res, result;
        return regeneratorRuntime_default()().wrap(function _callee3$(_context3) {
          while (1) switch (_context3.prev = _context3.next) {
            case 0:
              _this.serverConnection.settings.baseUrl;
              _context3.prev = 1;
              _context3.next = 4;
              return _this.serverConnection.makeRequest("".concat(_this.serverConnection.settings.baseUrl, "libro/api/execution"), {
                method: 'POST',
                body: JSON.stringify({
                  args: args,
                  file: _this.path
                })
              });
            case 4:
              res = _context3.sent;
              _context3.next = 7;
              return res.json();
            case 7:
              result = _context3.sent;
              _this.executionId = result.id;
              _this.executing = true;
              if (_this.libroView) {
                _this.libroView.dispose();
              }
              _this.libroView = undefined;
              _this.updateStatus();
              _context3.next = 18;
              break;
            case 15:
              _context3.prev = 15;
              _context3.t0 = _context3["catch"](1);
              console.log(_context3.t0);
            case 18:
            case "end":
              return _context3.stop();
          }
        }, _callee3, null, [[1, 15]]);
      }));
      return function (_x) {
        return _ref3.apply(this, arguments);
      };
    }();
    _this.doUpdateStatus = /*#__PURE__*/asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee4() {
      var res, result;
      return regeneratorRuntime_default()().wrap(function _callee4$(_context4) {
        while (1) switch (_context4.prev = _context4.next) {
          case 0:
            _context4.next = 2;
            return _this.serverConnection.makeRequest("".concat(_this.serverConnection.settings.baseUrl, "libro/api/execution?id=").concat(_this.executionId), {
              method: 'GET'
            });
          case 2:
            res = _context4.sent;
            _context4.next = 5;
            return res.json();
          case 5:
            result = _context4.sent;
            _this.count = result.cell_count;
            _this.currentIndex = result.current_index;
            if (!result.end_time) {
              _context4.next = 11;
              break;
            }
            _this.executing = false;
            return _context4.abrupt("return", true);
          case 11:
            return _context4.abrupt("return", false);
          case 12:
          case "end":
            return _context4.stop();
        }
      }, _callee4);
    }));
    _this.updateStatus = /*#__PURE__*/asyncToGenerator_default()( /*#__PURE__*/regeneratorRuntime_default()().mark(function _callee5() {
      return regeneratorRuntime_default()().wrap(function _callee5$(_context5) {
        while (1) switch (_context5.prev = _context5.next) {
          case 0:
            _context5.next = 2;
            return _this.doUpdateStatus();
          case 2:
            if (_context5.sent) {
              _context5.next = 8;
              break;
            }
            _context5.next = 5;
            return (0,promise_util/* timeout */.V)(1000);
          case 5:
            return _context5.abrupt("return", _this.updateStatus());
          case 8:
            _this.updateExecutionResult();
          case 9:
          case "end":
            return _context5.stop();
        }
      }, _callee5);
    }));
    return _this;
  }
  createClass_default()(LibroExecutionView, [{
    key: "path",
    get: function get() {
      return this._path;
    },
    set: function set(v) {
      this._path = v;
      this.update();
    }
  }]);
  return LibroExecutionView;
}(default_view/* BaseView */.P), (execution_view_descriptor = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "serverConnection", [execution_view_dec3], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor2 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "fileService", [execution_view_dec4], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor3 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "libroService", [execution_view_dec5], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor4 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "libroView", [execution_view_dec6], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor5 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "schema", [execution_view_dec7], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), execution_view_descriptor6 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "resultView", [_dec8], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor7 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "executionId", [_dec9], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
}), _descriptor8 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "executing", [_dec10], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: function initializer() {
    return false;
  }
}), _descriptor9 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "count", [_dec11], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: function initializer() {
    return 0;
  }
}), _descriptor10 = applyDecoratedDescriptor_default()(execution_view_class2.prototype, "currentIndex", [_dec12], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: function initializer() {
    return 0;
  }
})), execution_view_class2)) || execution_view_class) || execution_view_class);
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/view/slot.js
var slot = __webpack_require__(42681);
;// CONCATENATED MODULE: ./src/pages/execution/layout.tsx




var layout_dec, layout_dec2, layout_class;







var LibroExecutionLayoutSlots = {
  header: 'libro-execution-header',
  content: 'libro-execution-content'
};
var LibroExecutionLayoutComponent = /*#__PURE__*/(0,react.forwardRef)(function LibroExecutionLayoutComponent() {
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-execution-layout",
    children: /*#__PURE__*/(0,jsx_runtime.jsxs)(mana_react_es/* BoxPanel */.jN, {
      direction: "top-to-bottom",
      children: [/*#__PURE__*/(0,jsx_runtime.jsx)(mana_react_es/* BoxPanel */.jN.Pane, {
        className: "libro-lab-layout-header",
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(slot/* Slot */.g, {
          name: LibroExecutionLayoutSlots.header
        })
      }), /*#__PURE__*/(0,jsx_runtime.jsx)(mana_react_es/* BoxPanel */.jN.Pane, {
        className: "libro-lab-layout-container",
        flex: 1,
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(slot/* Slot */.g, {
          name: LibroExecutionLayoutSlots.content
        })
      })]
    })
  });
});
var LibroExecutionLayoutView = (layout_dec = (0,mana_syringe_es/* singleton */.ri)(), layout_dec2 = (0,decorator/* view */.ei)('libro-execution-layout'), layout_dec(layout_class = layout_dec2(layout_class = /*#__PURE__*/function (_BaseView) {
  inherits_default()(LibroExecutionLayoutView, _BaseView);
  var _super = createSuper_default()(LibroExecutionLayoutView);
  function LibroExecutionLayoutView() {
    var _this;
    classCallCheck_default()(this, LibroExecutionLayoutView);
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(args));
    _this.view = LibroExecutionLayoutComponent;
    return _this;
  }
  return createClass_default()(LibroExecutionLayoutView);
}(default_view/* BaseView */.P)) || layout_class) || layout_class);
;// CONCATENATED MODULE: ./src/pages/execution/execution-file.tsx








var execution_file_dec, execution_file_dec2, execution_file_dec3, execution_file_class, execution_file_class2, execution_file_descriptor;




var LibroExecutionFileComponent = /*#__PURE__*/(0,react.forwardRef)(function LibroExecutionFileComponent(props, ref) {
  var queryParams = query_string/* default */.Z.parse(window.location.search);
  var instance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var filePath = queryParams['path'];
  (0,react.useEffect)(function () {
    if (filePath && typeof filePath === 'string') {
      instance.path = filePath;
    }
  }, [filePath]);
  if (!queryParams['path']) {
    return null;
  }
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-execution-file",
    ref: ref,
    children: /*#__PURE__*/(0,jsx_runtime.jsx)("h2", {
      children: instance.path
    })
  });
});
var LibroExecutionFileView = (execution_file_dec = (0,mana_syringe_es/* singleton */.ri)(), execution_file_dec2 = (0,decorator/* view */.ei)('libro-execution-file'), execution_file_dec3 = (0,mana_observable_es/* prop */.vg)(), execution_file_dec(execution_file_class = execution_file_dec2(execution_file_class = (execution_file_class2 = /*#__PURE__*/function (_BaseView) {
  inherits_default()(LibroExecutionFileView, _BaseView);
  var _super = createSuper_default()(LibroExecutionFileView);
  function LibroExecutionFileView() {
    var _this;
    classCallCheck_default()(this, LibroExecutionFileView);
    for (var _len = arguments.length, args = new Array(_len), _key = 0; _key < _len; _key++) {
      args[_key] = arguments[_key];
    }
    _this = _super.call.apply(_super, [this].concat(args));
    _this.view = LibroExecutionFileComponent;
    initializerDefineProperty_default()(_this, "_path", execution_file_descriptor, assertThisInitialized_default()(_this));
    return _this;
  }
  createClass_default()(LibroExecutionFileView, [{
    key: "path",
    get: function get() {
      return this._path;
    },
    set: function set(v) {
      this._path = v;
    }
  }]);
  return LibroExecutionFileView;
}(default_view/* BaseView */.P), (execution_file_descriptor = applyDecoratedDescriptor_default()(execution_file_class2.prototype, "_path", [execution_file_dec3], {
  configurable: true,
  enumerable: true,
  writable: true,
  initializer: null
})), execution_file_class2)) || execution_file_class) || execution_file_class);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/slicedToArray.js
var slicedToArray = __webpack_require__(5574);
var slicedToArray_default = /*#__PURE__*/__webpack_require__.n(slicedToArray);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/objectSpread2.js
var objectSpread2 = __webpack_require__(97857);
var objectSpread2_default = /*#__PURE__*/__webpack_require__.n(objectSpread2);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/objectWithoutProperties.js
var objectWithoutProperties = __webpack_require__(13769);
var objectWithoutProperties_default = /*#__PURE__*/__webpack_require__.n(objectWithoutProperties);
// EXTERNAL MODULE: ./node_modules/@difizen/libro-core/es/index.js + 273 modules
var libro_core_es = __webpack_require__(59445);
// EXTERNAL MODULE: ./node_modules/antd/es/back-top/index.js + 4 modules
var back_top = __webpack_require__(21142);
// EXTERNAL MODULE: ./node_modules/@ant-design/icons/es/icons/ToTopOutlined.js + 1 modules
var ToTopOutlined = __webpack_require__(75162);
// EXTERNAL MODULE: ./node_modules/classnames/index.js
var classnames = __webpack_require__(93967);
var classnames_default = /*#__PURE__*/__webpack_require__.n(classnames);
// EXTERNAL MODULE: ./node_modules/@umijs/babel-preset-umi/node_modules/@babel/runtime/helpers/typeof.js
var helpers_typeof = __webpack_require__(52677);
var typeof_default = /*#__PURE__*/__webpack_require__.n(helpers_typeof);
// EXTERNAL MODULE: ./node_modules/react-dnd/dist/hooks/useDragDropManager.js
var useDragDropManager = __webpack_require__(21403);
// EXTERNAL MODULE: ./node_modules/react-dnd/dist/hooks/useDrag/useDrag.js + 9 modules
var useDrag = __webpack_require__(98958);
// EXTERNAL MODULE: ./node_modules/react-dnd/dist/hooks/useDrop/useDrop.js + 9 modules
var useDrop = __webpack_require__(98169);
// EXTERNAL MODULE: ./node_modules/react-dnd-html5-backend/dist/getEmptyImage.js
var getEmptyImage = __webpack_require__(23295);
// EXTERNAL MODULE: ./node_modules/resize-observer-polyfill/dist/ResizeObserver.es.js
var ResizeObserver_es = __webpack_require__(91033);
;// CONCATENATED MODULE: ./src/pages/execution/default-dnd-content.tsx



/* eslint-disable react-hooks/exhaustive-deps */








var AppCellContainer = function AppCellContainer(_ref) {
  var _instance$container;
  var cell = _ref.cell,
    index = _ref.index;
  var ref = (0,react.useRef)(null);
  var instance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var cellService = (0,mana_observable_es/* useInject */.oC)(libro_jupyter_es/* LibroCellService */.lt3);
  var dragDropManager = (0,useDragDropManager/* useDragDropManager */.N)();
  var dragDropMonitor = dragDropManager.getMonitor();
  var ItemRender = (0,mana_observable_es/* getOrigin */.P$)(instance.dndItemRender);
  (0,react.useLayoutEffect)(function () {
    if (typeof_default()(ref) !== 'object') {
      return function () {
        //
      };
    }
    var el = ref === null || ref === void 0 ? void 0 : ref.current;
    if (!el) {
      return function () {
        //
      };
    }
    var resizeObserver = new ResizeObserver(function (entries) {
      entries.forEach(function (entry) {
        var isVisible = entry.contentRect.width !== 0 && entry.contentRect.height !== 0;
        if (isVisible) {
          var _ref$current;
          cell.noEditorAreaHeight = ((_ref$current = ref.current) === null || _ref$current === void 0 ? void 0 : _ref$current.clientHeight) || 0;
        }
      });
    });
    resizeObserver.observe(el);
    return function () {
      cell.noEditorAreaHeight = 0;
      resizeObserver.disconnect();
    };
  }, [ref, cell]);
  var handleFocus = (0,react.useCallback)(function (e) {
    var className = e.target.className;
    if (e.target.tagName === 'svg' || className && className && typeof className === 'string' && (className.includes('mana-toolbar-item') || className.includes('mana-toolbar'))) {
      return;
    }
    instance.model.selectCell(cell);
    instance.model.selections = [];
    if (cell.shouldEnterEditorMode(e)) {
      instance.enterEditMode();
    }
  }, [instance, cell]);
  var handleMouseDown = (0,react.useCallback)(function (e) {
    instance.model.mouseMode = 'mouseDown';
  }, [instance, index]);
  var handleMouseUp = (0,react.useCallback)(function () {
    if (instance.model.mouseMode === 'multipleSelection' || instance.model.mouseMode === 'drag') {
      return;
    }
    instance.model.selectCell(cell);
    instance.model.selections = [];
  }, [instance, cell]);
  var scrollTimer = (0,react.useRef)(null);
  var unsubscribe = (0,react.useRef)(null);
  var _useDrag = (0,useDrag/* useDrag */.c)({
      type: libro_jupyter_es/* DragAreaKey */.CbU,
      item: {
        cell: cell,
        index: index
      },
      collect: function collect(monitor) {
        return {
          isDrag: monitor.isDragging()
        };
      },
      end: function end() {
        instance.isDragging = false;
        if (scrollTimer.current) {
          clearInterval(scrollTimer.current);
        }
      }
    }, [cell, index]),
    _useDrag2 = slicedToArray_default()(_useDrag, 3),
    isDrag = _useDrag2[0].isDrag,
    drag = _useDrag2[1],
    preview = _useDrag2[2];
  var libroViewContent = (_instance$container = instance.container) === null || _instance$container === void 0 || (_instance$container = _instance$container.current) === null || _instance$container === void 0 ? void 0 : _instance$container.getElementsByClassName('libro-view-content')[0];
  (0,react.useEffect)(function () {
    unsubscribe.current = dragDropMonitor.subscribeToStateChange(function () {
      instance.isDragging = dragDropMonitor.isDragging();
      scrollTimer.current = setInterval(function () {
        var currentOffset = dragDropMonitor.getClientOffset();
        if (libroViewContent && instance.isDragging && currentOffset) {
          var libroViewClientRect = libroViewContent.getBoundingClientRect();
          var top = libroViewClientRect.top,
            bottom = libroViewClientRect.bottom;
          var y = currentOffset.y;
          var topLimit = top + 30;
          var bottomLimit = bottom - 50;
          if (y < topLimit) {
            libroViewContent.scrollTop -= 0.5;
          } else if (y > bottomLimit) {
            libroViewContent.scrollTop += 0.5;
          }
        }
      }, 10);
      return function () {
        if (scrollTimer.current) {
          clearInterval(scrollTimer.current);
        }
        if (unsubscribe.current) {
          unsubscribe.current();
        }
      };
    });
  }, [dragDropMonitor]);
  (0,react.useEffect)(function () {
    // This gets called after every render, by default
    // (the first one, and every one after that)

    // Use empty image as a drag preview so browsers don't draw it
    // and we can draw whatever we want on the custom drag layer instead.
    preview((0,getEmptyImage/* getEmptyImage */.r)(), {
      // IE fallback: specify that we'd rather screenshot the node
      // when it already knows it's being dragged so we can hide it with CSS.
      captureDraggingState: true
    });
  }, [preview]);
  var _useDrop = (0,useDrop/* useDrop */.L)({
      accept: libro_jupyter_es/* DragAreaKey */.CbU,
      drop: function drop(item, monitor) {
        cellService.getOrCreateView(objectSpread2_default()(objectSpread2_default()({}, item.cell.model.options), {}, {
          modelId: item.cell.model.id,
          singleSelectionDragPreview: true
        }), item.cell.parent.id).then(function (view) {
          view.dispose();
          return;
        })["catch"](function (e) {
          //
        });
        if ((0,libro_jupyter_es/* isCellView */.CZ3)(item.cell)) {
          var didDrop = monitor.didDrop();
          if (didDrop) {
            return;
          }
          var dragIndex = instance.findCellIndex(item.cell);
          var dropIndex = instance.findCellIndex(cell);
          if (instance.model.selections.length > 0) {
            var isDragInSelections = instance.model.selections.findIndex(function (selection) {
              return selection.id === item.cell.id;
            }) > -1 ? true : false;
            var isDropInSelections = instance.model.selections.findIndex(function (selection) {
              return selection.id === cell.id;
            }) > -1 ? true : false;
            if (isDragInSelections && isDropInSelections) {
              return;
            }
            if (isDragInSelections) {
              instance.model.exchangeCells(instance.model.selections, dropIndex);
              instance.model.scrollToView(cell);
              return;
            }
          }
          if (dragIndex < dropIndex) {
            instance.model.exchangeCell(dragIndex, dropIndex - 1);
            instance.model.scrollToView(cell);
          }
          if (dragIndex > dropIndex) {
            instance.model.exchangeCell(dragIndex, dropIndex);
            instance.model.scrollToView(cell);
          }
        }
        return;
      },
      collect: function collect(monitor) {
        return {
          isDragOver: monitor.isOver(),
          canDrop: monitor.canDrop(),
          handlerId: monitor.getHandlerId()
        };
      }
    }),
    _useDrop2 = slicedToArray_default()(_useDrop, 2),
    _useDrop2$ = _useDrop2[0],
    handlerId = _useDrop2$.handlerId,
    isDragOver = _useDrop2$.isDragOver,
    drop = _useDrop2[1];
  var opacity = isDrag ? 0.4 : 1;
  if (!instance.model.readOnly) {
    drop(ref);
  }
  if (isDrag) {
    instance.model.mouseMode = 'drag';
  }
  var isMultiSelected = instance.model.selections.length !== 0 && instance.isSelected(cell);
  // let isMouseOver = false;
  var _useState = (0,react.useState)(false),
    _useState2 = slicedToArray_default()(_useState, 2),
    isMouseOverDragArea = _useState2[0],
    setIsMouseOverDragArea = _useState2[1];
  var hasCellHidden = (0,react.useMemo)(function () {
    return cell.hasCellHidden();
  }, [cell]);
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-dnd-cell-container ".concat(isMultiSelected ? 'multi-selected' : '', " ").concat(hasCellHidden ? 'hidden' : ''),
    "data-handler-id": handlerId,
    style: {
      opacity: opacity
    },
    ref: ref,
    id: cell.id,
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-drag-area",
      ref: drag,
      onMouseDown: handleMouseDown,
      onMouseUp: handleMouseUp,
      onMouseOver: function onMouseOver() {
        return setIsMouseOverDragArea(true);
      },
      onMouseLeave: function onMouseLeave() {
        return setIsMouseOverDragArea(false);
      }
    }), /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      tabIndex: -1,
      onFocus: handleFocus
      // onClick={e => e.preventDefault()}
      ,
      className: "libro-dnd-cell-content",
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(ItemRender, {
        isDragOver: !!isDragOver,
        isDrag: !!isDrag,
        cell: cell,
        isMouseOverDragArea: isMouseOverDragArea
      })
    })]
  });
};
// EXTERNAL MODULE: ./node_modules/@difizen/mana-core/es/configuration/hooks.js
var hooks = __webpack_require__(13684);
;// CONCATENATED MODULE: ./src/pages/execution/dnd-cell-item-render.tsx

/* eslint-disable react-hooks/exhaustive-deps */






var CellInputContent = /*#__PURE__*/(0,react.memo)(function CellInputContent(props) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var CellExecutionTime = (0,mana_observable_es/* useInject */.oC)(libro_jupyter_es/* CellExecutionTimeProvider */.fyr);
  var CellInputBottonBlank = (0,mana_observable_es/* useInject */.oC)(libro_jupyter_es/* CellInputBottonBlankProvider */.$iz);
  if (!(observableCell !== null && observableCell !== void 0 && observableCell.view) || !(0,libro_jupyter_es/* isCellView */.CZ3)(observableCell)) {
    return null;
  }
  var isHidden = observableCell.hasInputHidden;
  if (isHidden) {
    return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-input-hidden",
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(libro_jupyter_es/* ContentMore */.eoC, {})
    });
  }
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-cell-input-content",
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)(CellExecutionTime, {
      cell: cell
    }), /*#__PURE__*/(0,jsx_runtime.jsx)(view_render/* ViewRender */.o, {
      view: observableCell
    }), /*#__PURE__*/(0,jsx_runtime.jsx)(CellInputBottonBlank, {
      cell: cell
    })]
  });
});
var CellInputInnner = /*#__PURE__*/(0,react.forwardRef)(function CellInput(props, ref) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var _useConfigurationValu = (0,hooks/* useConfigurationValue */.K)(libro_jupyter_es/* CollapserClickActive */.gfq),
    _useConfigurationValu2 = slicedToArray_default()(_useConfigurationValu, 1),
    collapserClickActive = _useConfigurationValu2[0];
  var handleCellInputCollapser = function handleCellInputCollapser() {
    if (collapserClickActive) {
      observableCell.hasInputHidden = !observableCell.hasInputHidden;
    }
  };
  // TODO: 性能！
  // const isFirstCell = cell.parent.model.cells.indexOf(cell) === 0 ? true : false;
  var isFirstCell = (0,react.useMemo)(function () {
    return observableCell.parent.model.cells[0] && (0,mana_observable_es/* equals */.fS)(observableCell.parent.model.cells[0], observableCell) ? true : false;
  }, [observableCell]);
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-cell-container",
    tabIndex: 10,
    ref: ref,
    children: /*#__PURE__*/(0,jsx_runtime.jsx)(CellInputContent, {
      cell: observableCell
    })
  });
});
var CellInput = /*#__PURE__*/(0,react.memo)(CellInputInnner);
var CellOutputContent = /*#__PURE__*/(0,react.memo)(function CellOutputContent(props) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var CellOutputVisulization = (0,mana_observable_es/* useInject */.oC)(libro_jupyter_es/* CellOutputVisulizationProvider */.hdu);
  if (!libro_jupyter_es/* ExecutableCellView */.q0L.is(cell) || !libro_jupyter_es/* ExecutableCellView */.q0L.is(observableCell)) {
    return null;
  }
  if (!libro_jupyter_es/* ExecutableCellModel */.oM$.is(observableCell.model)) {
    return null;
  }
  var hasOutputsScrolled = observableCell.model.hasOutputsScrolled;
  var isHidden = observableCell.model.hasOutputHidden;
  if (isHidden) {
    return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-cell-output-hidden",
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(libro_jupyter_es/* ContentMore */.eoC, {})
    });
  }
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-cell-output-content ".concat(hasOutputsScrolled ? 'scrolled' : '', " "),
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)(CellOutputVisulization, {
      cell: cell
    }), /*#__PURE__*/(0,jsx_runtime.jsx)(view_render/* ViewRender */.o, {
      view: cell.outputArea
    })]
  });
});
var LibroCellExecutionTime = /*#__PURE__*/(/* unused pure expression or super */ null && (forwardRef(function LibroCellExecutionTime() {
  return null;
})));
var LibroCellInputBottonBlank = /*#__PURE__*/(/* unused pure expression or super */ null && (forwardRef(function LibroCellInputBottonBlank() {
  return null;
})));
var LibroCellVisualization = /*#__PURE__*/(/* unused pure expression or super */ null && (forwardRef(function LibroCellVisualization() {
  return null;
})));
var CellOutput = /*#__PURE__*/(0,react.forwardRef)(function CellOutput(props, ref) {
  var _cell$outputArea;
  var cell = props.cell;
  var outputRef = (0,react.useRef)(null);
  var isExecutingRef = (0,react.useRef)(null);
  var executing = false;
  if (libro_jupyter_es/* ExecutableCellModel */.oM$.is(cell.model)) {
    executing = cell.model.executing;
  }
  (0,react.useLayoutEffect)(function () {
    isExecutingRef.current = !!executing;
  }, [executing]);
  if (!libro_jupyter_es/* ExecutableCellView */.q0L.is(cell)) {
    return null;
  }
  if (!(0,libro_jupyter_es/* isCellView */.CZ3)(cell) || !libro_jupyter_es/* ExecutableCellModel */.oM$.is(cell.model) || !((_cell$outputArea = cell.outputArea) !== null && _cell$outputArea !== void 0 && _cell$outputArea.length)) {
    return null;
  }
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-cell-output-container",
    ref: ref,
    children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      ref: outputRef,
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(CellOutputContent, {
        cell: cell
      })
    })
  });
});
var DndCellItemContent = /*#__PURE__*/(0,react.memo)(function DndCellItemContent(props) {
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  if (cell.model.type === 'markdown') {
    return /*#__PURE__*/(0,jsx_runtime.jsx)(CellInput, {
      cell: observableCell
    });
  } else {
    return /*#__PURE__*/(0,jsx_runtime.jsx)(CellOutput, {
      cell: observableCell
    });
  }
});
var DndCellItemRenderInner = /*#__PURE__*/(0,react.forwardRef)(function DndCellItemRender(props, ref) {
  var _instance$activeCell;
  var cell = props.cell;
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var instance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var isActive = ((_instance$activeCell = instance.activeCell) === null || _instance$activeCell === void 0 ? void 0 : _instance$activeCell.id) === observableCell.id;
  var hasErrorOutputs = (0,libro_jupyter_es/* hasErrorOutput */.DJ7)(observableCell);
  var hasCellHidden = (0,react.useMemo)(function () {
    return observableCell.hasCellHidden();
  }, [observableCell]);
  var classNames = ['libro-dnd-cell', {
    'command-mode': instance.model.commandMode
  }, {
    'edit-mode': !instance.model.commandMode
  }, {
    error: hasErrorOutputs
  }, {
    hidden: hasCellHidden
  }];
  if (observableCell.wrapperCls) {
    classNames.push(observableCell.wrapperCls);
  }
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-dnd-cell-border",
    children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: classnames_default()(classNames),
      ref: ref,
      children: /*#__PURE__*/(0,jsx_runtime.jsx)(DndCellItemContent, {
        cell: cell
      })
    })
  });
});
var DndCellItemRender = /*#__PURE__*/(0,react.memo)(DndCellItemRenderInner);
;// CONCATENATED MODULE: ./src/pages/execution/libro-app-view.tsx







var libro_app_view_dec, libro_app_view_dec2, libro_app_view_class;
var _excluded = ["cell", "index"];
















var DndCellRender = /*#__PURE__*/(0,react.memo)(function DndCellRender(_ref) {
  var cell = _ref.cell,
    index = _ref.index,
    props = objectWithoutProperties_default()(_ref, _excluded);
  var observableCell = (0,mana_observable_es/* useObserve */.Re)(cell);
  var instance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var DndCellContainer = instance.dndContentRender;
  return /*#__PURE__*/(0,jsx_runtime.jsx)(DndCellContainer, objectSpread2_default()({
    cell: observableCell,
    index: index
  }, props), cell.id);
});
var DndCellsRender = /*#__PURE__*/(0,react.forwardRef)(function DndCellsRender(_ref2, ref) {
  var libroView = _ref2.libroView,
    addCellButtons = _ref2.addCellButtons;
  var LoadingRender = (0,mana_observable_es/* getOrigin */.P$)(libroView.loadingRender);
  var virtualizedManagerHelper = (0,mana_observable_es/* useInject */.oC)(libro_core_es/* VirtualizedManagerHelper */.rj);
  var virtualizedManager = virtualizedManagerHelper.getOrCreate(libroView.model);
  var cells = libroView.model.getCells().reduce(function (a, b) {
    if (a.indexOf(b) < 0) {
      a.push(b);
    }
    return a;
  }, []);
  var _useState = (0,react.useState)(false),
    _useState2 = slicedToArray_default()(_useState, 2),
    isVirtualList = _useState2[0],
    setIsVirtualList = _useState2[1];
  var _useState3 = (0,react.useState)(true),
    _useState4 = slicedToArray_default()(_useState3, 2),
    isJudging = _useState4[0],
    setIsJudging = _useState4[1];
  (0,react.useEffect)(function () {
    if (!libroView.model.isInitialized) {
      return;
    }
    var size = undefined;
    var path = undefined;

    // TODO: 类型处理
    var model = libroView.model;
    if (model.currentFileContents && model.currentFileContents.size) {
      size = parseFloat((model.currentFileContents.size / 1048576).toFixed(3)); // 单位MB
      path = model.currentFileContents.path || '';
    }
    setIsJudging(true);
    virtualizedManager.openVirtualized(cells.length, size, path).then(function (willOpen) {
      setIsVirtualList(willOpen);
      return;
    })["catch"](function () {
      setIsVirtualList(false);
    })["finally"](function () {
      setIsJudging(false);
    })["catch"](function (e) {
      //
    });
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [virtualizedManager, libroView.model.isInitialized]);
  var isInitialized = libroView.model.isInitialized;
  var isLoading = !isInitialized || isJudging;
  var shouldRenderCells = isInitialized && !isJudging;
  return /*#__PURE__*/(0,jsx_runtime.jsx)(jsx_runtime.Fragment, {
    children: /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
      className: classnames_default()('libro-dnd-cells-container'),
      ref: ref,
      children: [isLoading && /*#__PURE__*/(0,jsx_runtime.jsx)(LoadingRender, {}), shouldRenderCells && /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
        style: {
          height: '100%',
          overflow: 'visible'
        },
        children: cells.filter(function (cell) {
          return !cell.collapsedHidden;
        }).map(function (cell, index) {
          return /*#__PURE__*/(0,jsx_runtime.jsx)(DndCellRender, {
            cell: cell,
            index: index
          }, cell.id);
        })
      })]
    })
  });
});
var LibroAppComponent = /*#__PURE__*/(0,react.memo)(function LibroAppComponent() {
  var ref = (0,react.useRef)(null);
  var libroViewTopRef = (0,react.useRef)(null);
  var libroViewRightContentRef = (0,react.useRef)(null);
  var libroViewLeftContentRef = (0,react.useRef)(null);
  var libroViewContentRef = (0,react.useRef)(null);
  var instance = (0,mana_observable_es/* useInject */.oC)(view_protocol/* ViewInstance */.yd);
  var handleScroll = (0,react.useCallback)(function () {
    var _instance$container, _instance$activeCell, _instance$activeCell2, _instance$activeCell3, _activeOutput$outputs, _instance$activeCell4, _libroViewTopRef$curr;
    instance.cellScrollEmitter.fire();
    var cellRightToolbar = (_instance$container = instance.container) === null || _instance$container === void 0 || (_instance$container = _instance$container.current) === null || _instance$container === void 0 ? void 0 : _instance$container.getElementsByClassName('libro-cell-right-toolbar')[instance.model.activeIndex];
    var activeCellOffsetY = (_instance$activeCell = instance.activeCell) === null || _instance$activeCell === void 0 || (_instance$activeCell = _instance$activeCell.container) === null || _instance$activeCell === void 0 || (_instance$activeCell = _instance$activeCell.current) === null || _instance$activeCell === void 0 ? void 0 : _instance$activeCell.getBoundingClientRect().y;
    var activeCellOffsetRight = (_instance$activeCell2 = instance.activeCell) === null || _instance$activeCell2 === void 0 || (_instance$activeCell2 = _instance$activeCell2.container) === null || _instance$activeCell2 === void 0 || (_instance$activeCell2 = _instance$activeCell2.current) === null || _instance$activeCell2 === void 0 ? void 0 : _instance$activeCell2.getBoundingClientRect().right;
    var activeOutput = libro_jupyter_es/* ExecutableCellView */.q0L.is(instance.activeCell) && ((_instance$activeCell3 = instance.activeCell) === null || _instance$activeCell3 === void 0 ? void 0 : _instance$activeCell3.outputArea);
    var activeOutputOffsetBottom = activeOutput && activeOutput.length > 0 ? activeOutput === null || activeOutput === void 0 || (_activeOutput$outputs = activeOutput.outputs[activeOutput.length - 1].container) === null || _activeOutput$outputs === void 0 || (_activeOutput$outputs = _activeOutput$outputs.current) === null || _activeOutput$outputs === void 0 ? void 0 : _activeOutput$outputs.getBoundingClientRect().bottom : (_instance$activeCell4 = instance.activeCell) === null || _instance$activeCell4 === void 0 || (_instance$activeCell4 = _instance$activeCell4.container) === null || _instance$activeCell4 === void 0 || (_instance$activeCell4 = _instance$activeCell4.current) === null || _instance$activeCell4 === void 0 ? void 0 : _instance$activeCell4.getBoundingClientRect().bottom;
    var libroViewTopOffsetBottom = (_libroViewTopRef$curr = libroViewTopRef.current) === null || _libroViewTopRef$curr === void 0 ? void 0 : _libroViewTopRef$curr.getBoundingClientRect().bottom;
    if (!cellRightToolbar) {
      return;
    }
    if (activeCellOffsetY !== undefined && libroViewTopOffsetBottom !== undefined && activeOutputOffsetBottom !== undefined && activeCellOffsetY <= libroViewTopOffsetBottom + 12 && activeOutputOffsetBottom >= libroViewTopOffsetBottom && activeCellOffsetRight !== undefined) {
      cellRightToolbar.style.cssText = "position:fixed;top:".concat(libroViewTopOffsetBottom + 12, "px;left:").concat(activeCellOffsetRight + 44 - 34, "px;right:unset;");
    } else {
      cellRightToolbar.style.cssText = '  position: absolute;top: 0px;right: -44px;';
    }
  }, [instance]);
  return /*#__PURE__*/(0,jsx_runtime.jsxs)("div", {
    className: "libro-view-content",
    onScroll: handleScroll,
    ref: libroViewContentRef,
    children: [/*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-view-content-left",
      ref: libroViewLeftContentRef,
      children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
        className: "libro-dnd-list-container",
        children: /*#__PURE__*/(0,jsx_runtime.jsxs)(libro_jupyter_es/* DndContext */.LBT, {
          children: [/*#__PURE__*/(0,jsx_runtime.jsx)(libro_jupyter_es/* CustomDragLayer */.Bhd, {}), /*#__PURE__*/(0,jsx_runtime.jsx)(DndCellsRender, {
            libroView: instance,
            addCellButtons: null
          })]
        })
      })
    }), /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
      className: "libro-view-content-right",
      ref: libroViewRightContentRef
    }), /*#__PURE__*/(0,jsx_runtime.jsx)(back_top/* default */.Z, {
      target: function target() {
        return libroViewContentRef.current || document;
      },
      children: /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
        className: "libro-totop-button",
        children: /*#__PURE__*/(0,jsx_runtime.jsx)(es_button/* default */.ZP, {
          shape: "circle",
          icon: /*#__PURE__*/(0,jsx_runtime.jsx)(ToTopOutlined/* default */.Z, {})
        })
      })
    })]
  });
});
var LibroAppView = (libro_app_view_dec = (0,mana_syringe_es/* transient */.H3)(), libro_app_view_dec2 = (0,decorator/* view */.ei)(libro_core_es/* notebookViewFactoryId */.QS), libro_app_view_dec(libro_app_view_class = libro_app_view_dec2(libro_app_view_class = /*#__PURE__*/function (_LibroJupyterView) {
  inherits_default()(LibroAppView, _LibroJupyterView);
  var _super = createSuper_default()(LibroAppView);
  function LibroAppView(options, collapseServiceFactory, notebookService, virtualizedManagerHelper) {
    var _this;
    classCallCheck_default()(this, LibroAppView);
    _this = _super.call(this, options, collapseServiceFactory, notebookService, virtualizedManagerHelper);
    _this.view = LibroAppComponent;
    _this.dndContentRender = AppCellContainer;
    _this.dndItemRender = DndCellItemRender;
    _this.uri = void 0;
    return _this;
  }
  LibroAppView = (0,mana_syringe_es/* inject */.f3)(libro_core_es/* VirtualizedManagerHelper */.rj)(LibroAppView, undefined, 3) || LibroAppView;
  LibroAppView = (0,mana_syringe_es/* inject */.f3)(libro_core_es/* NotebookService */.yE)(LibroAppView, undefined, 2) || LibroAppView;
  LibroAppView = (0,mana_syringe_es/* inject */.f3)(libro_core_es/* CollapseServiceFactory */.Se)(LibroAppView, undefined, 1) || LibroAppView;
  LibroAppView = (0,mana_syringe_es/* inject */.f3)(view_protocol/* ViewOption */.Hj)(LibroAppView, undefined, 0) || LibroAppView;
  createClass_default()(LibroAppView, [{
    key: "options",
    get: function get() {
      return this.model.options;
    }
  }]);
  return LibroAppView;
}(libro_jupyter_es/* LibroJupyterView */.lKf)) || libro_app_view_class) || libro_app_view_class);
;// CONCATENATED MODULE: ./src/pages/execution/index.tsx









var BaseModule = mana_module/* ManaModule */.R.create().register(LibroApp, LibroExecutionView, LibroExecutionLayoutView, LibroExecutionFileView, libro_lab_es/* BrandView */.S5, LibroAppView, (0,decorator/* createSlotPreference */.vk)({
  slot: view_protocol/* RootSlotId */.lI,
  view: LibroExecutionLayoutView
}), (0,decorator/* createSlotPreference */.vk)({
  slot: LibroExecutionLayoutSlots.header,
  view: header_view/* HeaderView */.m
}), (0,decorator/* createSlotPreference */.vk)({
  slot: header_view/* HeaderArea */.M.middle,
  view: LibroExecutionFileView
}), (0,decorator/* createSlotPreference */.vk)({
  slot: header_view/* HeaderArea */.M.left,
  view: libro_lab_es/* BrandView */.S5
}), (0,decorator/* createSlotPreference */.vk)({
  slot: LibroExecutionLayoutSlots.content,
  view: LibroExecutionView
}));
var LibroExecution = function LibroExecution() {
  return /*#__PURE__*/(0,jsx_runtime.jsx)("div", {
    className: "libro-execution",
    children: /*#__PURE__*/(0,jsx_runtime.jsx)(components/* ManaComponents */.rF.Application, {
      asChild: true,
      modules: [es/* ManaAppPreset */.n6L, libro_jupyter_es/* LibroJupyterModule */.MDs, BaseModule]
    }, "libro-execution")
  });
};
/* harmony default export */ var execution = (LibroExecution);

/***/ }),

/***/ 22868:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 14777:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 99830:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 70209:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 87414:
/***/ (function() {

/* (ignored) */

/***/ }),

/***/ 13769:
/***/ (function(module, __unused_webpack_exports, __webpack_require__) {

var objectWithoutPropertiesLoose = __webpack_require__(48541);
function _objectWithoutProperties(source, excluded) {
  if (source == null) return {};
  var target = objectWithoutPropertiesLoose(source, excluded);
  var key, i;
  if (Object.getOwnPropertySymbols) {
    var sourceSymbolKeys = Object.getOwnPropertySymbols(source);
    for (i = 0; i < sourceSymbolKeys.length; i++) {
      key = sourceSymbolKeys[i];
      if (excluded.indexOf(key) >= 0) continue;
      if (!Object.prototype.propertyIsEnumerable.call(source, key)) continue;
      target[key] = source[key];
    }
  }
  return target;
}
module.exports = _objectWithoutProperties, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ }),

/***/ 48541:
/***/ (function(module) {

function _objectWithoutPropertiesLoose(source, excluded) {
  if (source == null) return {};
  var target = {};
  var sourceKeys = Object.keys(source);
  var key, i;
  for (i = 0; i < sourceKeys.length; i++) {
    key = sourceKeys[i];
    if (excluded.indexOf(key) >= 0) continue;
    target[key] = source[key];
  }
  return target;
}
module.exports = _objectWithoutPropertiesLoose, module.exports.__esModule = true, module.exports["default"] = module.exports;

/***/ })

}]);