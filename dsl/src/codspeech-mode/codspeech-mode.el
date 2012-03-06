;; Authors:
;; Viktor Almqvist
;; Martin Hardselius

;; This mode is under development

(defvar codspeech-mode-hook nil)

(defvar codspeech-mode-map
  (let ((map (make-keymap)))
    (define-key map "\C-j" 'newline-and-indent)
    map)
  "Keymap for codspeach major mode")

;; autoload
;;(add-to-list 'auto-mode-alist '("\\.cod'" . codspeech-mode))
(setq auto-mode-alist (cons '("\\.cod$" . codspeech-mode) auto-mode-alist))

;;------------------------------------------------------------------------------
;; Syntax highlighting using keywords
;;------------------------------------------------------------------------------

(defvar codspeech-font-lock-keywords 
  (list
    '("/\#[^/]*?\#/" . font-lock-comment-face)
    '("\#[^\\\n]*" . font-lock-comment-face)
    '("'''.*?'''" . font-lock-string-face)
    '("\<[^>]*?\>" . font-lock-preprocessor-face)
    '("\\<\\(import\\|Component\\|Network\\|Controller\\|Atom\\)\\>" . font-lock-keyword-face)
;    '("\\('\\w*'\\)" . font-lock-variable-name-face)
;    '("\\<\\(out\\|in\\)\\>" . font-lock-constant-face)
    '("[A-Z][a-zA-Z]*" . font-lock-type-face)
    '("Component \\([a-z][a-zA-Z0-9]*\\)" . (1 font-lock-function-name-face)))
  "Default highlighting expressions for codspeech mode")

;;------------------------------------------------------------------------------
;; indent?
;;------------------------------------------------------------------------------


;;------------------------------------------------------------------------------
;; Syntax table
;;------------------------------------------------------------------------------

(defvar codspeech-mode-syntax-table
  (let ((st (make-syntax-table)))

  (modify-syntax-entry ?_ "w" st)

;  (modify-syntax-entry ?/# "<" st)
;  (modify-syntax-entry ?#/ ">" st)

;  (modify-syntax-entry ?/ ". 14" st)
;  (modify-syntax-entry ?# ". 23" st)

;  (modify-syntax-entry ?' "\"" st)

  st)
  "Syntax table for codspeech-mode")

;;------------------------------------------------------------------------------
;; The entry funciton
;;------------------------------------------------------------------------------

(defun codspeech-mode ()
  "Major mode for editing codspeech files"
  (interactive)
  (kill-all-local-variables)
  (set-syntax-table codspeech-mode-syntax-table)
  (use-local-map codspeech-mode-map)

  (set (make-local-variable 'font-lock-defaults) '(codspeech-font-lock-keywords))

;;  (set (make-local-variable 'indent-line-function) 'codspeech-indent-line)

  (setq major-mode 'codspeech-mode)
  (setq mode-name "CodSpeech")
  (run-hooks 'codspeech-mode-hook))

(provide 'codspeech-mode)