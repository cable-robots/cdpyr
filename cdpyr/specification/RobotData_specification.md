## Data Model

### XML-Structure - robot

```xml
<robot version"1.0", name="copacabana">
    <frame>
        ...
    </frame>
    <platforms>
        <platform id="0">
        </platform>
        <platform id="1">
        </platform>
        ...
    </platforms>
    <connectivity>
        <chains>
        </chains>
        <platforms>
        </platforms>
    </connectivity>
    <cables>
        <cable id="0", type="standard">
        </cable>
        <cable id="1", type="standard">
        </cable>
        ...
    </cables>  
</robot>
```

#### XML-Structure - frame

```xml
<frame>
    <anchors>
        <anchor id="0">
            <position x="0", y="0", z="0">
            </position>
            <orientation R11="1", R12="0", R13="0", R21="0", R22="1", R23="0", R31="0", R23="0", R33="1">
            </orientation>  
            <pulley>
                <orientation R11="1", R12="0", R13="0", R21="0", R22="1", R23="0", R31="0", R23="0", R33="1">
                </orientation>
                <radius r="0.1">
                </radius>
                <inertia m="0.1" J="0.001">
                </inertia>
            </pulley>  
    </anchors>
    <drive_train>
        <winch>
            <radius r="0.1">
            </radius>
            <inertia m="0.1" J="0.001">
            </inertia>
        </winch>
        <gearbox>
            <ratio i="12">
            </ratio>
            <inertia m="0.1" J="0.001">
            </inertia>                      
        </gearbox>
        <motor>
            <max_torque t="50">
            </max_torque>
            <inertia J="0.005">
            </inertia>
        </motor>
    </drive_train>
</frame>
```
#### XML-Structure - platform

```xml
<platform motion_pattern="3R3T", spatiality="true", body_type="">
    <anchors>
      <anchor id="0">
        <position x="0", y="0", z="0">
        </position>
        <orientation R11="1", R12="0", R13="0", R21="0", R22="1", R23="0", R31="0", R23="0", R33="1">
        </orientation>
      </anchor>
    </anchors>
    <linear_intertia m="5">
    <inertia m="5", J="0.1">
    </inertia>
    <cocs>
      <position x="0", y="0", z="0">
      </position>
      <orientation R11="1", R12="0", R13="0", R21="0", R22="1", R23="0", R31="0", R23="0", R33="1">
      </orientation>
    </cocs>
</platform>
```
#### XML-Structure - connectivity

```xml
<connectivity>
    <chains>
        <frame c0="0", c1="1", c2="2", c3="3", c4="4", c5="5", c6="6", c7="7">
        </frame>
        <platform id="0", c0="0", c1="1", c2="2", c3="3", c4="4", c5="5", c6="6", c7="7" >
        </platform>
    </chains>
    <platform>
    </platform>
</connectivity>
```
#### XML-Structure - cables

```xml
<cables>
    <cable id="0", type="standad", breaking_load="10000">
    </cable>
    <cable id="0", type="linear", E="10e9", breaking_load="10000">
    </cable>    
</cables>
```
