
function Obstacle(gl, a,x,y,z) {

    // Create a buffer for the cube's vertex positions.

    const positionBuffer = gl.createBuffer();

    // Select the positionBuffer as the one to apply buffer
    // operations to from here out.

    gl.bindBuffer(gl.ARRAY_BUFFER, positionBuffer);

    // Now create an array of positions for the cube.
    var positions = [];
    var i = 0;
    N = 1;

    this.x = x;
    this.y=y;
    this.z = z;
    x=0;y=0;z=0;
    j=0;
    var l=0;
    {
        //0
        positions[i++] = a * Math.cos(45 * 3.14 * j / 180)+x;
        positions[i++] = a * Math.sin(45 * 3.14 * j / 180)+y;
        positions[i++] = l+z;

        //1
        positions[i++] = a * Math.cos(45 * 3.14 * j / 180)+x;
        positions[i++] = a * Math.sin(45 * 3.14 * j / 180)+y;
        positions[i++] = l+z- a/2;

        //2
        positions[i++] = a * Math.cos(45 * 3.14 * (j+1/2) / 180)+x;
        positions[i++] = a * Math.sin(45 * 3.14 * (j+1/2) / 180)+y;
        positions[i++] = l+z;
        //3
        positions[i++] = a * Math.cos(45 * 3.14 * j+1/2 / 180)+x;
        positions[i++] = a * Math.sin(45 * 3.14 * (j+1/2) / 180)+y;
        positions[i++] = l+z- a/2;

        //4
        positions[i++] = -a * Math.cos(45 * 3.14 * j / 180)+x;
        positions[i++] = -a * Math.sin(45 * 3.14 * j / 180)+y;
        positions[i++] = l+z;

        //5
        positions[i++] = -a * Math.cos(45 * 3.14 * j / 180)+x;
        positions[i++] = -a * Math.sin(45 * 3.14 * j / 180)+y;
        positions[i++] = l+z- a/2;

        //6
        positions[i++] = -a * Math.cos(45 * 3.14 * (j+1/2) / 180)+x;
        positions[i++] = -a * Math.sin(45 * 3.14 * (j+1/2) / 180)+y;
        positions[i++] = l+z;
        //7
        positions[i++] = -a * Math.cos(45 * 3.14 * (j+1/2) / 180)+x;
        positions[i++] = -a * Math.sin(45 * 3.14 * (j+1/2) / 180)+y;
        positions[i++] = l+z- a/2;


    }


    // Now pass the list of positions into WebGL to build the
    // shape. We do this by creating a Float32Array from the
    // JavaScript array, then use it to fill the current buffer.

    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(positions), gl.STATIC_DRAW);

    // Now set up the colors for the faces. We'll use solid colors
    // for each face.

    const textureCoordBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ARRAY_BUFFER, textureCoordBuffer);

    const textureCoordinates = [
        // Front
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,
        // Back
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,
        // Top
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,
        // Bottom
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,
        // Right
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,
        // Left
        0.0, 0.0,
        1.0, 0.0,
        1.0, 1.0,
        0.0, 1.0,

       
    ];

    gl.bufferData(gl.ARRAY_BUFFER, new Float32Array(textureCoordinates),
        gl.STATIC_DRAW);


    // Build the element array buffer; this specifies the indices
    // into the vertex arrays for each face's vertices.

    const indexBuffer = gl.createBuffer();
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, indexBuffer);

    // This array defines each face as two triangles, using the
    // indices into the vertex array to specify each triangle's
    // position.

    var indices = []
    i = 0;
    var idx = 0
    {
        //one side
        indices[i++] = 0;
        indices[i++] = 1 ;
        indices[i++] = 3 ;

        indices[i++] = 0 ;
        indices[i++] = 2 ;
        indices[i++] = 3 ;

        indices[i++] = 0;
        indices[i++] = 4;
        indices[i++] = 6;

        indices[i++] = 0;
        indices[i++] = 2;
        indices[i++] = 4;

        indices[i++] = 0;
        indices[i++] = 1;
        indices[i++] = 7;

        indices[i++] = 0;
        indices[i++] = 6;
        indices[i++] = 7;

        //other side
        indices[i++] = 1;
        indices[i++] = 7;
        indices[i++] = 5;

        indices[i++] = 1;
        indices[i++] = 5;
        indices[i++] = 3;

        indices[i++] = 2;
        indices[i++] = 4;
        indices[i++] = 5;

        indices[i++] = 2;
        indices[i++] = 3;
        indices[i++] = 5;
//
        indices[i++] = 6;
        indices[i++] = 4;
        indices[i++] = 5;

        indices[i++] = 6;
        indices[i++] = 7;
        indices[i++] = 5;    
    }

    // Now send the element array to GL

    gl.bufferData(gl.ELEMENT_ARRAY_BUFFER,
        new Uint16Array(indices), gl.STATIC_DRAW);

    this.buffers = {
        position: positionBuffer,
        textureCoord: textureCoordBuffer,
        index: indexBuffer,
    };

    this.obsRotation =0;
    this.rotation  = Math.random()/15;
    if(Math.random()<0.3)
        this.rotation = -this.rotation;
        
}


Obstacle.prototype.draw = function (gl, programInfo, deltaTime, projectionMatrix,cameraMatrix,rotation) {

    const modelViewMatrix = mat4.create();
    mat4.multiply(modelViewMatrix, cameraMatrix, modelViewMatrix);
    
    mat4.translate(modelViewMatrix,     // destination matrix
        modelViewMatrix,     // matrix to translate
        [this.x, this.y, this.z]);  // amount to translate

    this.obsRotation += this.rotation;
    mat4.rotate(modelViewMatrix,  // destination matrix
        modelViewMatrix,  // matrix to rotate
        this.obsRotation,     // amount to rotate in radians
        [0,0,1]);       // axis to rotate around (Z)

    
    buffers = this.buffers;
    {
        const numComponents = 3;
        const type = gl.FLOAT;
        const normalize = false;
        const stride = 0;
        const offset = 0;
        gl.bindBuffer(gl.ARRAY_BUFFER, buffers.position);
        gl.vertexAttribPointer(
            programInfo.attribLocations.vertexPosition,
            numComponents,
            type,
            normalize,
            stride,
            offset);
        gl.enableVertexAttribArray(
            programInfo.attribLocations.vertexPosition);
    }
    // Tell WebGL how to pull out the colors from the color buffer
    // into the vertexColor attribute.
    {
        const num = 2; // every coordinate composed of 2 values
        const type = gl.FLOAT; // the data in the buffer is 32 bit float
        const normalize = false; // don't normalize
        const stride = 0; // how many bytes to get from one set to the next
        const offset = 0; // how many bytes inside the buffer to start from
        gl.bindBuffer(gl.ARRAY_BUFFER, this.buffers.textureCoord);
        gl.vertexAttribPointer(
            programInfo.attribLocations.textureCoord,
            num,
            type,
            normalize,
            stride,
            offset);
        gl.enableVertexAttribArray(programInfo.attribLocations.textureCoord);
    }
    // Tell WebGL which indices to use to indices the vertices
    gl.bindBuffer(gl.ELEMENT_ARRAY_BUFFER, buffers.index);

    // Tell WebGL to use our program when drawing

    gl.useProgram(programInfo.program);

    // Set the shader uniforms
    // Tell WebGL we want to affect texture unit 0
    gl.activeTexture(gl.TEXTURE0);

    // Bind the texture to texture unit 0
    gl.bindTexture(gl.TEXTURE_2D, obstacle_texture);


    gl.uniformMatrix4fv(
        programInfo.uniformLocations.projectionMatrix,
        false,
        projectionMatrix);
    gl.uniformMatrix4fv(
        programInfo.uniformLocations.modelViewMatrix,
        false,
        modelViewMatrix);

    {
        const vertexCount = 36;
        const type = gl.UNSIGNED_SHORT;
        const offset = 0;
        gl.drawElements(gl.TRIANGLES, vertexCount, type, offset);
    }

}