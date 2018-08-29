(($) ->
  $.widget "salsita.clipthru",

    # TODO
    # add an option to create new clones on collision instead of precaching
    # add SVG mask/clipPath support for Chrome and IE as maskOriginal
  
    # webkit doesn't support a real svg mask element, just an alpha channel object
    # https://mdn.mozillademos.org/files/2665/clipdemo.xhtml
    # http://stackoverflow.com/questions/4817999/svg-clippath-to-clip-the-outer-content-out
    # http://stackoverflow.com/questions/20237594/clip-path-web-kit-mask-works-when-svg-is-seperate-file-but-not-when-inline?rq=1
    # http://thenittygritty.co/css-masking
    # http://stackoverflow.com/questions/20600608/svg-mask-tag-required-for-firefox-but-appears-to-break-css-mask-in-chrome
    # http://collidercreative.com/how-to-create-css-image-masks-for-the-web-with-svgs/

    options:
      collisionTarget: null
      keepClonesInHTML: false
      removeAttrOnClone: ['id']
      blockSource: null
      maskOriginal: true
      updateOnScroll: true
      updateOnResize: true
      updateOnZoom: true
      updateOnCSSTransitionEnd: false
      autoUpdate: false
      autoUpdateInterval: 100
      debug: false

    _create: ->
      @dataAttribute = 'jq-clipthru'
      @overlayOffset = null
      if @options.collisionTarget
        @collisionTarget = $(@element.find(@options.collisionTarget).get(0))
      else
        @collisionTarget = @element
      @collisionTargetOffset = null
      @allBlocks = null
      @allClones = null
      @collidingBlocks = []
      @svgMaskInitialized = false
      @_initWidget()

    _initWidget: ->
      _self = this
      @_getAllBlocks()
      if @allBlocks.length > 0
        @_logMessage "#{@allBlocks.length} blocks found", @allBlocks
        @collisionTarget.addClass "#{@dataAttribute}-origin"
        @_addIdToBlocks()
        @_attachListeners()
        @_createOverlayClones()
        @refresh()
        clearInterval @autoUpdateTimer?
        if @options.autoUpdate
          @autoUpdateTimer = setInterval (->
            _self.refresh()
          ), @options.autoUpdateInterval
      else
        @_logMessage 'no blocks found'

    _triggerEvent: (name, data) ->
      @element.trigger name, [data]
      @_logMessage name, data

    _logMessage: (name, args) ->
      if @options.debug
        console.debug "#{@dataAttribute}: #{name}", args

    # Get all existing blocks.
    _getAllBlocks: ->
      if @options.blockSource
        for cls, blocks of @options.blockSource
          for block in blocks
            $(block).data @dataAttribute, cls
            if @allBlocks
              @allBlocks = @allBlocks.add $(block)
            else
              @allBlocks = $(block)
      else
        @allBlocks = $("[data-#{@dataAttribute}]")

    # Get offsets of the overlay element.
    _getOverlayOffset: ->
      @overlayOffset = @element.get(0).getBoundingClientRect()
      @collisionTargetOffset = @collisionTarget.get(0).getBoundingClientRect()

    # Give each block a specific id so it's easier to manage the overlay clones.
    _addIdToBlocks: ->
      i = 0
      _self = this
      @allBlocks.each ->
        $(this).data "#{_self.dataAttribute}-id", i
        i++

    # Create an overlay clone for each potential block and keep it cached.
    _createOverlayClones: ->
      _self = this
      @allBlocks.each ->
        clone = _self.element.clone()
        if _self.options.removeAttrOnClone
          for attr in _self.options.removeAttrOnClone
            clone.removeAttr attr
        clone.addClass "#{_self.dataAttribute}-clone"
        clone.addClass $(this).data _self.dataAttribute
        clone.data "#{_self.dataAttribute}-id", $(this).data("#{_self.dataAttribute}-id")
        if _self.allClones
          _self.allClones = _self.allClones.add clone
        else
          _self.allClones = clone
      if @options.keepClonesInHTML
        @allClones.insertAfter @element
      @_triggerEvent "clonesCreated.#{@dataAttribute}", @allClones

    # Show or hide the colliding overlay clones.
    _updateOverlayClones: ->
      _self = this
      @allClones.each ->
        id = $(this).data("#{_self.dataAttribute}-id")
        if _self.collidingBlocks.hasOwnProperty id
          if _self.options.keepClonesInHTML
            $(this).css
              display: _self.element.css 'display'
          else
            if not document.body.contains this
              $(this).insertAfter _self.element
          _self._clipOverlayClone this, _self._getCollisionArea(_self.collidingBlocks[id])
          if _self.options.maskOriginal
            _self._manageOriginMask()
        else
          if _self.options.keepClonesInHTML
            $(this).css
              display: 'none'
          else
            $(this).detach()

      if @collidingBlocks.length is 0
        @element.css
          'clip': 'rect(auto auto auto auto)'

    # Calculate the collision offset values for CSS clip.
    _getCollisionArea: (blockOffset) ->
      clipOffset = []
      clipOffset.push @overlayOffset.height - (@overlayOffset.bottom - blockOffset.top)
      clipOffset.push blockOffset.right - @overlayOffset.left
      clipOffset.push blockOffset.bottom - @overlayOffset.top
      clipOffset.push @overlayOffset.width - (@overlayOffset.right - blockOffset.left)
      return clipOffset
    
    # Calculate collision area relative to collision target.
    _getRelativeCollisionArea: (bl, cl) ->
      obj =
        x: 0
        y: 0
        width: 0
        height: 0
      # Get X axis position.
      if bl.left > cl.left
        obj.x = bl.left - cl.left
      # Get Y axis position.
      if bl.top > cl.top
        obj.y = bl.top - cl.top
      # Get width.
      objWidth = 0
      blRight = bl.left + bl.width
      clRight = cl.left + cl.width
      if blRight < clRight
        # Possible .5 pixel rounding errors, not overly important given it's used on a transparent element.
        objWidth = clRight - blRight
      obj.width = cl.width - obj.x - objWidth
      # Get height.
      objHeight = 0
      blBottom = bl.top + bl.height
      clBottom = cl.top + cl.height
      if blBottom < clBottom
        objHeight = clBottom - blBottom
      obj.height = cl.height - obj.y - objHeight
      return obj

    # Return ids for blocks that collide with the overlay.
    _getCollidingBlocks: ->
      _self = this
      @collidingBlocksOld = @collidingBlocks
      @collidingBlocks = []
      @allBlocks.each ->
        wasCollidedBefore = _self.collidingBlocksOld.hasOwnProperty($(this).data("#{_self.dataAttribute}-id"))
        # Does the block collide with the overlay?
        blockOffset = this.getBoundingClientRect()
        if (blockOffset.bottom >= _self.collisionTargetOffset.top) and
        (blockOffset.top <= _self.collisionTargetOffset.bottom) and
        (blockOffset.left <= _self.collisionTargetOffset.right) and
        (blockOffset.right >= _self.collisionTargetOffset.left)
          _self.collidingBlocks[$(this).data("#{_self.dataAttribute}-id")] = blockOffset
          if !wasCollidedBefore
            delayEvent = -> _self._triggerEvent "collisionStart.#{_self.dataAttribute}", this
            setTimeout delayEvent, 0
        else if wasCollidedBefore
          delayEvent = -> _self._triggerEvent "collisionEnd.#{_self.dataAttribute}", this
          setTimeout delayEvent, 0

    _clipOverlayClone: (clone, offset) ->
      $(clone).css
        'clip': "rect(#{offset[0]}px #{offset[1]}px #{offset[2]}px #{offset[3]}px)"

    _clipOverlayOriginal: (offset) ->
      @element.css
        'clip': "rect(#{offset[0]}px auto #{offset[1]}px auto)"
        
    _manageOriginMask: ->
      _self = this
      
      manageSVGObject = ->
        _self.element.css
          'mask': 'none'
        $("##{_self.dataAttribute}-origin-mask-wrapper").remove()
        if _self.collidingBlocks.length > 0
          collisionMask = ''
          # Generate a black rectangular mask for each collision.
          for block, i in _self.collidingBlocks
            if _self.collidingBlocks.hasOwnProperty i
              collisionMask = collisionMask +
                "<rect
                   id='#{_self.dataAttribute}-origin-mask-rect-#{i}'
                   x='0'
                   y='0'
                   width='0'
                   height='0'
                   fill='black'/>"
          # Create the SVG object and add to DOM.
          maskTemplate = $("<svg id='#{_self.dataAttribute}-origin-mask-wrapper' height='0' style='position: absolute; z-index: -1;'>
                              <defs>
                                <mask id='#{_self.dataAttribute}-origin-mask'>
                                  <rect id='#{_self.dataAttribute}-origin-mask-fill' x='0' y='0' width='0' height='0' fill='white' />
                                  #{collisionMask}
                                </mask>
                              </defs>
                            </svg>")
          $('body').append maskTemplate
          # Apply the Firefox luminance mask.
          _self.element.css
            'mask': "url(##{_self.dataAttribute}-origin-mask)"
      
      # Update SVG mask attributes with real data.
      updateSVGProperties = ->
        maskFill = $("##{_self.dataAttribute}-origin-mask-fill")
        maskFill.attr 'width', _self.collisionTargetOffset.width
        maskFill.attr 'height', _self.collisionTargetOffset.height
        for block, i in _self.collidingBlocks
          if _self.collidingBlocks.hasOwnProperty i
            maskRect = $("##{_self.dataAttribute}-origin-mask-rect-#{i}")
            # Get mask dimensions.
            maskDimensions = _self._getRelativeCollisionArea block, _self.collisionTargetOffset
            maskRect.attr 'x', maskDimensions.x
            maskRect.attr 'y', maskDimensions.y
            maskRect.attr 'width', maskDimensions.width
            maskRect.attr 'height', maskDimensions.height
      
      if @svgMaskInitialized
        # Just change attributes of the SVG mask.
        updateSVGProperties()
      else
        # Create a new SVG object in the DOM.
        manageSVGObject()
        # Bind to recreate the SVG object on collision update. 
        @element.on "collisionStart.#{_self.dataAttribute} collisionEnd.#{_self.dataAttribute}", (e) ->
          manageSVGObject()
          updateSVGProperties()
        @svgMaskInitialized = true

    _attachListeners: ->
      _self = this
      $(window).on "#{'resize.' + @dataAttribute if @options.updateOnResize} #{'scroll.' + @dataAttribute if @options.updateOnScroll}", ->
        _self.refresh()

      if @options.updateOnCSSTransitionEnd
        @element.on 'transitionend webkitTransitionEnd oTransitionEnd otransitionend MSTransitionEnd', (event) ->
          if event.originalEvent.propertyName is _self.options.updateOnCSSTransitionEnd
            _self.refresh()

    refresh: ->
      @_getOverlayOffset()
      @_getCollidingBlocks()
      @_updateOverlayClones()

    _destroy: ->
      $(window).off "resize.#{@dataAttribute} scroll.#{@dataAttribute}"
      @element.off()
      clearInterval @autoUpdateTimer
      @element.css
        'clip': 'auto auto auto auto'
      @allClones.remove()
      @allBlocks = null
      @allClones = null
      @overlayOffset = null
      @collisionTarget = null
      @collisionTargetOffset = null
      @collidingBlocks = null
      @collidingBlocksOld = null

) jQuery