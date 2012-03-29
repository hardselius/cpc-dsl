;; Authors:
;; Viktor Almqvist
;; Martin Hardselius

;; This mode is under development

(defvar codspeech-mode-hook nil)

(defvar codspeech-mode-map
  (let ((map (make-keymap)))
;    (define-key map "\C-j" 'newline-and-indent)
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
    '("\#[^\\\n]*" . font-lock-comment-face)
    '("'''\\(.\\|\n\\)*?'''" . font-lock-string-face)
    '("\\<\\(import\\|in\\|out\\|network\\|atom\\|type\\|options\\)\\>" . font-lock-keyword-face)
    '("atom[ ]+\\(external\\|python-extended\\|python\\)[ ]+\\([a-z][a-zA-Z0-9]*\\)" (1 'font-lock-keyword-face) (2 'font-lock-function-name-face))
    '("network[ ]+\\([a-z][a-zA-Z0-9]*\\)" . (1 'font-lock-function-name-face))
    '("type[ ]*\\([a-z][_A-Za-z-]*\\)" . (1 'font-lock-type-face))
    '("[(,][ ]*\\([a-z][_A-Za-z-]*\\)[ :]+[a-z][a-zA-Z0-9]*" . (1 font-lock-type-face))
    '("[=(][ ]*\\([a-z][a-zA-Z0-9]*\\)[ ]*(" . (1 font-lock-function-name-face))
	'("\\(controller\\)[ ]*([ ]*\\([a-z][a-zA-Z0-9]*\\)[ ]*)" (1 font-lock-builtin-face) (2 font-lock-function-name-face))
    '("\\<\\(true\\|false\\)\\>" . font-lock-constant-face))
  "Default highlighting expressions for codspeech mode")

;;------------------------------------------------------------------------------
;; indent?
;;------------------------------------------------------------------------------

;(defun codspeech-indent-line ()
;  "Indent current line as codspeech code."
;  (interactive)
;  (beginning-of-line)
;  (if (bobp)
;	  (indent-line-to 0))		   ; First line is always non-indented
;  (if (looking-at "^[ ]*in]")
;	  (indent-line-to 1)))

;	(let ((not-indented t) cur-indent)
;	  (if (looking-at "^[ ]*[})]") ; If the line we are looking at is the end of a block, then decrease the indentation
;		  (progn
;			(save-excursion
;			  (forward-line -1)
;			  (setq cur-indent (- (current-indentation) default-tab-width)))
;			(if (< cur-indent 0) ; We can't indent past the left margin
;				(setq cur-indent 0)))
;		(save-excursion
;		  (while not-indented ; Iterate backwards until we find an indentation hint
;			(forward-line -1)
;			(if (looking-at "^[ ]*[)}]") ; This hint indicates that we need to indent at the level of the END_ token
;				(progn
;				  (setq cur-indent (current-indentation))
;				  (setq not-indented nil))
;			  (if (looking-at "^[ ]*\\(atom\\|(\\|network\\)") ; This hint indicates that we need to indent an extra level
;				  (progn
;					(setq cur-indent (+ (current-indentation) default-tab-width)) ; Do the actual indenting
;					(setq not-indented nil))
;				(if (bobp)
;					(setq not-indented nil)))))))
;	  (if cur-indent
;		  (indent-line-to cur-indent)
;		(indent-line-to 0))))) ; If we didn't see an indentation hint, then allow no indentation

;;------------------------------------------------------------------------------
;; Syntax table
;;------------------------------------------------------------------------------

(defvar codspeech-mode-syntax-table
  (let ((st (make-syntax-table)))
;    (modify-syntax-entry ?_ "w" st)
    (modify-syntax-entry ?/ ". 14" st)
    (modify-syntax-entry ?# ". 23" st)
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

;  (set (make-local-variable 'indent-line-function) 'codspeech-indent-line)

  (setq major-mode 'codspeech-mode)
  (setq mode-name "CodSpeech")
  (run-hooks 'codspeech-mode-hook))

(provide 'codspeech-mode)