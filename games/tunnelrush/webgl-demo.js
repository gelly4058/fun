var cubeRotation = 0.0;
var move_flag = 0;

var Camera = {
  x: 0,
  y: 0,
  z: 0,
}

var pos;
var x;
var x_shift = 0.05;
var cam_z = 0;
var flag = 0;
var ABC;
var obstacles = [];
var a = 2;
var gl;
var tun = [];
var canvas;
var c = 0;
var tunnels = [];
var boxNo = 0;
var obs_probability = 0.01;

main();

//
// Start here
//
//
tunnel_texture = loadTexture(gl, 'text.jpg');
obstacle_texture = loadTexture(gl,'dot.jpg');

function main() {
  canvas = document.querySelector('#glcanvas');
  gl = canvas.getContext('webgl') || canvas.getContext('experimental-webgl');

  // If we don't have a GL context, give up now
  document.addEventListener('keydown', keyDownHandler, false);

  function keyDownHandler(event) {
    if (event.keyCode == 39) {

      cubeRotation -= 8;
    }

    else if (event.keyCode == 37) {

      cubeRotation += 8;
    }
  }


  if (!gl) {
    alert('Unable to initialize WebGL. Your browser or machine may not support it.');
    return;
  }
  // Vertex shader program

  const vsSource = `
    attribute vec4 aVertexPosition;
    attribute vec2 aTextureCoord;

    uniform mat4 uModelViewMatrix;
    uniform mat4 uProjectionMatrix;

    varying highp vec2 vTextureCoord;

    void main(void) {
      gl_Position = uProjectionMatrix * uModelViewMatrix * aVertexPosition;
      vTextureCoord = aTextureCoord;
    }
  `;

  // Fragment shader program

  const fsSource = `
    varying highp vec2 vTextureCoord;

    uniform sampler2D uSampler;

    void main(void) {
      gl_FragColor = texture2D(uSampler, vTextureCoord);
    }
  `;

  // Initialize a shader program; this is where all the lighting
  // for the vertices and so forth is established.
  const shaderProgram = initShaderProgram(gl, vsSource, fsSource);

  // Collect all the info needed to use the shader program.
  // Look up which attributes our shader program is using
  // for aVertexPosition, aVevrtexColor and also
  // look up uniform locations.
  const programInfo = {
    program: shaderProgram,
    attribLocations: {
      vertexPosition: gl.getAttribLocation(shaderProgram, 'aVertexPosition'),
      textureCoord: gl.getAttribLocation(shaderProgram, 'aTextureCoord'),
    },
    uniformLocations: {
      projectionMatrix: gl.getUniformLocation(shaderProgram, 'uProjectionMatrix'),
      modelViewMatrix: gl.getUniformLocation(shaderProgram, 'uModelViewMatrix'),
      uSampler: gl.getUniformLocation(shaderProgram, 'uSampler'),
    },
  };

  // Here's where we call the routine that builds all the
  // objects we'll be drawing.


  var then = 0;

  var N = 100;
  pos = 0;
  x = 0;
  for (var j = 0; j < N; j++) {
    tun.push((createTunnel(gl, a, x, pos)));
    pos += a;
    x += 2 * x_shift;

  }

  



  // Draw the scene repeatedly

  function render(now) {
    now *= 0.001;  // convert to seconds
    const deltaTime = now - then;
    then = now;
    // console.log(Camera.z, c++);
    drawScene(gl, programInfo, tun, deltaTime);

    requestAnimationFrame(render);
  }
  requestAnimationFrame(render);
}

function createTunnel(gl, a, r, pos) {
  var tun;
  tun = new Tunnel(gl, a, r, pos);
  if(Math.random()<obs_probability)
  obstacles.push(new Obstacle(gl, a, r, 0, pos));
  
  return tun;
}



//
// Draw the scene.
//
var theta = 0;
var boxCnt = 0;
var prevBox = -1;
function drawScene(gl, programInfo, tun, deltaTime) {

  gl.clearColor(0.0, 0.0, 0.0, 1.0);  // Clear to black, fully opaque
  gl.clearDepth(1.0);                 // Clear everything
  gl.enable(gl.DEPTH_TEST);           // Enable depth testing
  gl.depthFunc(gl.LEQUAL);            // Near things obscure far things

  // Clear the canvas before we start drawing on it.

  gl.clear(gl.COLOR_BUFFER_BIT | gl.DEPTH_BUFFER_BIT);

  // Create a perspective matrix, a special matrix that is
  // used to simulate the distortion of perspective in a camera.
  // Our field of view is 45 degrees, with a width/height
  // ratio that matches the display size of the canvas
  // and we only want to see objects between 0.1 units
  // and 100 units away from the camera.

  const fieldOfView = 45 * Math.PI / 180;   // in radians
  const aspect = gl.canvas.clientWidth / gl.canvas.clientHeight;
  const zNear = 0.1;
  const zFar = 100.0;
  const projectionMatrix = mat4.create();

  var cameraMatrix = mat4.create();
  r = 1.4;
  // note: glmatrix.js always has the first argument
  // console.log(theta);
  const eye = [Camera.x + r * Math.sin(cubeRotation * Math.PI / 180), Camera.y + -r * Math.cos(cubeRotation * Math.PI / 180), Camera.z];
  const look = [Camera.x + Math.sin(theta) + r * Math.sin(cubeRotation * Math.PI / 180), Camera.y - r * Math.cos(cubeRotation * Math.PI / 180), Math.cos(theta) + Camera.z + 10];
  const up = [-Math.sin(cubeRotation * Math.PI / 180), Math.cos(cubeRotation * Math.PI / 180), 0];
  // as the destination to receive the result.


  mat4.lookAt(cameraMatrix, eye, look, up);

  

  mat4.perspective(projectionMatrix,
    fieldOfView,
    aspect,
    zNear,
    zFar);

 

  var ind = [];
  var j;
  var speed = deltaTime * 13;
  for (j = 0; j < tun.length; j++) {
    if (tun[j] != -1) {
      
      tun[j].draw(gl, programInfo, deltaTime, projectionMatrix,ABC , cameraMatrix);
        if (tun[j].z < Camera.z && tun[j].z + a * 9 / 10 > Camera.z) {
        var rat = tun[j+1].x - Camera.x;
        var cat = tun[j+1].z - Camera.z;
          theta = Math.atan(rat/cat);
          // console.log("x.tun",tun[j].x,"x.cam",Camera.x,"z.tun",tun[j].z,"z.cam",Camera.z,theta);
        if (prevBox < j) {
          boxCnt += 1;        // 
          prevBox = j;
          boxNo += 1;
        }
        
      }
    }
  }
  // console.log(speed * Math.sin(theta));
  Camera.x += speed * Math.sin(theta);        
  Camera.z += speed * Math.cos(theta);
  // console.log(tun.length);
  if(prevBox<=5)
  {
    
  }
  if (boxCnt > 10) {
    var n = 30;
    if ((tun.length / 10) % 2 == 1)
      x_shift = 0;
    else
      x_shift = 0.05;
    while (n--) {
      delete tun[prevBox - 1];
      tun[prevBox - 1] = -1;
      tun.push((createTunnel(gl, a, x, pos)));
      pos += a;
      x += 2 * x_shift;
     
    }
    obs_probability += 0.01;
    
    boxCnt = 0;

  }
  
  
  

  for (var k = 0; k < obstacles.length; k++)
  {
    obstacles[k].draw(gl, programInfo, deltaTime, projectionMatrix, cameraMatrix,0.03);
    console.log("drawn");
  }

}

//
// Initialize a shader program, so WebGL knows how to draw our data
//
function initShaderProgram(gl, vsSource, fsSource) {
  const vertexShader = loadShader(gl, gl.VERTEX_SHADER, vsSource);
  const fragmentShader = loadShader(gl, gl.FRAGMENT_SHADER, fsSource);

  // Create the shader program

  const shaderProgram = gl.createProgram();
  gl.attachShader(shaderProgram, vertexShader);
  gl.attachShader(shaderProgram, fragmentShader);
  gl.linkProgram(shaderProgram);

  // If creating the shader program failed, alert

  if (!gl.getProgramParameter(shaderProgram, gl.LINK_STATUS)) {
    alert('Unable to initialize the shader program: ' + gl.getProgramInfoLog(shaderProgram));
    return null;
  }
  return shaderProgram;
}

//
// creates a shader of the given type, uploads the source and
// compiles it.
//
function loadShader(gl, type, source) {
  const shader = gl.createShader(type);

  // Send the source to the shader object

  gl.shaderSource(shader, source);

  // Compile the shader program

  gl.compileShader(shader);

  // See if it compiled successfully

  if (!gl.getShaderParameter(shader, gl.COMPILE_STATUS)) {
    alert('An error occurred compiling the shaders: ' + gl.getShaderInfoLog(shader));
    gl.deleteShader(shader);
    return null;
  }
  return shader;
}

