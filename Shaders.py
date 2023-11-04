# Graphics Library Shader Language: GLSL

vertex_shader = """
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    uniform float time;
    
    out vec2 UVs;
    out vec3 normal;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        UVs = texCoords;
        normal = normalize(
            (modelMatrix * vec4(normals, 0.0)).xyz
        );
    }
"""

fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;
    
    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        fragColor = texture(tex, UVs);
    }
"""

dirtAndDamage_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;

    uniform float time;
    uniform float dirtiness; 
    uniform float damage; 

    in vec2 UVs;

    out vec4 fragColor;

   
    float random (vec2 co) {
        return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
    }

    void main() {
    
        vec4 textureColor = texture(tex, UVs);

      
        float dirt = random(UVs + time) * dirtiness;
        float damageValue = random(UVs - time) * damage;

       
        vec3 dirtLayer = vec3(dirt, dirt, dirt);
        vec3 damageLayer = vec3(damageValue, damageValue, damageValue);

        
        vec3 finalColor = textureColor.rgb * (1.0 - dirtiness) + dirtLayer * dirtiness - damageLayer;

        
        fragColor = vec4(finalColor, textureColor.a);
    }
"""