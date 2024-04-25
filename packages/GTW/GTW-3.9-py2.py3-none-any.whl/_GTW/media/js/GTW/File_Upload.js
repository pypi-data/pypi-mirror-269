/*
** Copyright (C) 2010 Martin Glueck All rights reserved
** Langstrasse 4, A--2244 Spannberg, Austria. martin@mangari.org
** ****************************************************************************
** This file is part of the library GTW.
**
** This module is licensed under the terms of the BSD 3-Clause License
** <https://www.gg32.com/license/bsd_3c.html>.
** ****************************************************************************
**
**++
** Name
**     GTW_File_Upload
**
** Purpose
**    Javascipt library for file upload via AJAX.
**
** Revision Dates
**    24-Jun-2010 (MG) Creation
**    ««revision-date»»···
**--
*/

(function ($)
{
  var _T;
  var _;
  var _Tn;

  if ($.I18N === undefined)
    {
      _T = _ = _Tn = function (t) { return t; }
    }
  else
    {
      _T = _ = $.I18N._T;
      _Tn    = $.I18N._Tn;
    }
  if ($.GTW_File_Upload === undefined)
    {
      function _File_Upload_ ()
        {
          this.max_simultaneous_uploads = 2;
          this.queue                    = [];
          this.running                  = 0;
          this._id                      = 0;
          this._running                 = {};
        };
      _File_Upload_.prototype.options = function (max_sim_upload)
        {
          this.max_simultaneous_uploads = max_sim_upload;
        }
      _File_Upload_.prototype.add = function ($input, url, callback, data)
        {
          this.queue.push
              ({input : $input, url : url, callback : callback, data : data});
          this._start_next_upload ();
        }
      _File_Upload_.prototype._start_next_upload = function ()
        {
          if (  this.running      < this.max_simultaneous_uploads
             && this.queue.length > 0
             )
            {
              this.running += 1;
              this._id     += 1;
              var  next   = this.queue.pop ();
              var  name   = "upload-frame-" + this._id;
              var  self   = this;
              var $iframe = $('<iframe></iframe>').attr ("name", name).hide ();
              var $form   = $( '<form action="' + next.url + '" '
                             + 'method="post" '
                             + 'enctype="multipart/form-data" '
                             + 'target="' + name + '">'
                             + '</form>'
                               ).append (next.input).hide ();
              $("body").append ($iframe).append ($form);
              // console.log ("Start a new upload");
              $iframe.load (function ()
                  {
                    self._upload_finished (this, $form);
                  }); //.hide ();
              this._running [name] = next;
              $form.submit ();
            }
        }
      _File_Upload_.prototype._upload_finished = function (frame, $form)
        {
          var upload   = this._running [frame.name];
          var callback = upload.callback;
          this.running -= 1;
          if (callback !== undefined)
            {
              var files = [];
              var $files = $(frame).contents ().find ("dd");
              for (var i = 0; i < $files.length; i++)
                {
                  var $name = $files.eq (i);
                  files.push ({field : $name.html (), file_name : $name.next ().html ()});
                }
              callback (files, upload.data);
            }
          $form.remove            ();
          /* remove the frame in a time because removing it in the load event
          ** causes Firefox 3 to never stop loading the frame
          ** see
          ** http://www.bennadel.com/blog/1336-FireFox-Never-Stops-Loading-With-iFrame-Submission.htm
          ** for more details
          */
          setTimeout (function () {$(frame).remove ()}, 50);
          // console.log             ("Upload finished");
          this._start_next_upload ();
        }
      $.GTW_File_Upload = Upload_Queue = new _File_Upload_;
    }

  var GTW_File_Upload =
    { options :
        { "upload_url" : "/upload/test/"
        }
    , _create : function ()
      { this.element.bind ("change", this, this._new_file);
      }
    , _new_file : function (evt)
      {
        var self   = evt.data;
        var $input = self.element;
        var $name  = $('<span class="gtw-upload-name gtw-uploading"></span>')
                     .html ($input.attr ("value"));
        $input.after ($name).remove ();
        Upload_Queue.add
            ( $input, self.options.upload_url, self._upload_complete
            , $name
            );
      }
      , _upload_complete : function (files, data)
      {
        var field     = files [0].field;
        var file_name = files [0].file_name;
        var $name     = data;
        var field     = '<input type="hidden" name="' + field
                      + '" value="' + file_name + '">';
        $name.removeClass ("gtw-uploading").after (field);
      }
    };

  $.widget ("ui.GTW_File_Upload", GTW_File_Upload);
  $.extend
      ( $.ui.GTW_Form
      , { "version"      : "0.1"
        }
      );
}) (jQuery);
