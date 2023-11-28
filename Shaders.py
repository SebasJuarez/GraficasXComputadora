# Graphics Library Shader Language: GLSL

vertex_shader = """
    #version 450 core
    layout (location = 0) in vec3 position;
    layout (location = 1) in vec2 texCoords;
    layout (location = 2) in vec3 normals;
    
    uniform mat4 modelMatrix;
    uniform mat4 viewMatrix;
    uniform mat4 projectionMatrix;
    
    out vec2 UVs;
    out vec3 normal;
    
    void main() {
        gl_Position = projectionMatrix * viewMatrix * modelMatrix * vec4(position, 1.0);
        UVs = texCoords;
        normal = (modelMatrix * vec4(normals, 0.0)).xyz;
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

gourad_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;

    uniform float lightIntensity;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;
    
    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;
        fragColor = texture(tex, UVs) * intensity;
    }
"""

dirt_fragment_shader = """
    #version 450 core
    
    layout (binding = 0) uniform sampler2D tex;

    uniform float time;
    uniform float dirtiness; 

    in vec2 UVs;

    out vec4 fragColor;

    float random (vec2 co) {
        return fract(sin(dot(co, vec2(12.9898, 78.233))) * 43758.5453);
    }

    void main() {
        vec4 textureColor = texture(tex, UVs);

        float dirt = random(UVs + time) * dirtiness;

        vec3 dirtLayer = vec3(dirt, dirt, dirt);

        vec3 finalColor = mix(textureColor.rgb, dirtLayer, dirtiness);

        fragColor = vec4(finalColor, textureColor.a);
    }
"""

noise_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;
    layout (binding = 1) uniform sampler2D noiseTex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float edgeSens = 0.4;
        float intensity = 0.85;

        float gouraudIntensity = dot(normal, -dirLight) * lightIntensity;

        vec2 noiseCoords = UVs + vec2(time * -0.1);
        float noise = texture(noiseTex, noiseCoords).r;
        vec2 distortedCoords = UVs + vec2(noise * 0.1 + sin(time) * 0.05);
        vec4 color = texture(tex, UVs) * gouraudIntensity;

        float gintensity = 0.2989 * color.r + 0.5870 * color.g + 0.1140 * color.b;
        
        if (noise > 0.8) {
            if (gintensity > edgeSens) {
                fragColor = color;
            } else if (gintensity > intensity) {
                fragColor = vec4(0, 0, 0, 1);
            } else {
                fragColor = vec4(0, 0, 0, 1);
            }
        } else {
            fragColor = texture(noiseTex, distortedCoords);
        }
    }

"""
tv_noise_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform float time;

    in vec2 UVs;
    out vec4 fragColor;

    // Function to generate pseudo-random numbers
    float rand(vec2 co) {
        return fract(sin(dot(co.xy, vec2(12.9898, 78.233))) * 43758.5453);
    }

    void main() {
        // Generate a random grayscale color with a time-dependent offset
        float gray = rand(UVs + vec2(time));
        vec3 color = vec3(gray, gray, gray);

        fragColor = vec4(color, 1.0);
    }
"""

stroboscopic_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;

        // Define the two colors to alternate between
        vec3 color1 = vec3(1.0, 0.0, 0.0); // Red
        vec3 color2 = vec3(0.0, 0.0, 1.0); // Blue

        // Calculate the stroboscopic color based on the time
        vec3 stroboscopicColor = mix(color1, color2, step(sin(time * 10.0), 0.0));

        fragColor = vec4(stroboscopicColor, 1.0) * intensity;
    }
"""

sparkling_fragment_shader = """

    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    uniform vec3 dirLight;
    uniform float lightIntensity;
    uniform float time;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    void main() {
        float intensity = dot(normal, -dirLight) * lightIntensity;

        // Muestrear la textura original en función de las coordenadas UV
        vec4 originalColor = texture(tex, UVs);

        // Agregar un movimiento cíclico a los colores usando el tiempo
        float cycleSpeed = 4.0; // Ajusta la velocidad del ciclo
        originalColor = originalColor * (1.0 + 0.5 * sin(time * cycleSpeed));

        fragColor = originalColor * vec4(vec3(1.0), 1.0) * intensity;
    }
"""

distorsioned_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    uniform float time; // Para controlar la animación del agua

    void main() {
        // Factor de distorsión para el agua
        float distortionFactor = 0.02;
        
        // Coordenadas de textura distorsionadas
        vec2 distortedUVs = UVs + vec2(
            sin(UVs.y * 10.0 + time) * distortionFactor,
            cos(UVs.x * 10.0 + time) * distortionFactor
        );
        
        // Mapeo de la textura distorsionada
        vec4 waterColor = texture(tex, distortedUVs);
        
        // Ajustar la transparencia para el efecto de ondulación
        waterColor.a = 0.7 + sin(UVs.x * 10.0 + time) * 0.1;
        
        fragColor = waterColor;
    }
"""

anime_style_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex;

    in vec2 UVs;
    in vec3 normal;
    out vec4 fragColor;

    uniform vec3 lightDir; // Direction of the light

    void main() {
        // Normalize the normal vector
        vec3 N = normalize(normal);

        // Calculate the dot product of the normal and light direction
        float dotProd = dot(N, lightDir);

        // Define the color bands
        vec3 color1 = vec3(0.1, 0.1, 0.1); // Dark color
        vec3 color2 = vec3(0.5, 0.5, 0.5); // Mid color
        vec3 color3 = vec3(1.0, 1.0, 1.0); // Light color

        // Apply the cel-shading effect
        if (dotProd < 0.33) {
            fragColor = vec4(color1, 1.0);
        } else if (dotProd < 0.66) {
            fragColor = vec4(color2, 1.0);
        } else {
            fragColor = vec4(color3, 1.0);
        }
    }
"""
break_fragment_shader = """
    #version 450 core

    layout (binding = 0) uniform sampler2D tex; // Original texture
    layout (binding = 1) uniform sampler2D crackTex; // Crack texture

    in vec2 UVs;
    out vec4 fragColor;

    void main() {
        vec4 textureColor = texture(tex, UVs);
        vec4 crackColor = texture(crackTex, UVs);

        // If the crack texture is black, show the original texture
        // If the crack texture is white, show a dark color (like a shadow inside the crack)
        if (crackColor.r > 0.5) {
            fragColor = vec4(0.0, 0.0, 0.0, 1.0); // Dark color
        } else {
            fragColor = textureColor;
        }
    }
"""