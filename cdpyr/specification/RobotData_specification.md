
# Data Model

## XML-Structure - robot

```xml
<robot>
    <version> 1.0 </version>
    <name> "copacabana" </name>
    <frame>
        ...
    </frame>
    <platforms>
        <platform>
            <id> 0 </id>
        </platform>
        <platform>
            <id> 1 </id>
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
        <cable>
            <id> 0 </id>
            <type> "standard" </type>
        </cable>
        <cable>
            <id> 0 </id>
            <type> "standard" </type>
        </cable>
        ...
    </cables>  
</robot>
```

## XML-Structure - frame

```xml
<frame>
    <anchors>
        <anchor>
            <id> 0 </id>
            <position>
                <x> 0 </x>
                <y> 0 </y>
                <z> 0 </z>
            </position>
            <orientation>
                <R11> 1 </R11>
                <R12> 0 </R12>
                <R13> 0 </R13>
                <R21> 0 </R21>
                <R22> 1 </R22>
                <R23> 0 </R23>
                <R31> 0 </R31>
                <R32> 0 </R32>
                <R33> 1 </R33>
            </orientation>  
            <pulley>
                <orientation>
                    <R11> 1 </R11>
                    <R12> 0 </R12>
                    <R13> 0 </R13>
                    <R21> 0 </R21>
                    <R22> 1 </R22>
                    <R23> 0 </R23>
                    <R31> 0 </R31>
                    <R32> 0 </R32>
                    <R33> 1 </R33>
                </orientation>
                <radius>
                    <r> 0.1 </r>
                </radius>
                <inertia>
                    <m> 0.1 </m>
                    <J> 0.001 </J>
                </inertia>
            </pulley>  
    </anchors>
    <drive_train>
        <winch>
            <radius>
                <r> 0.1 </r>
            </radius>
            <inertia>
                <m> 0.1 </m>
                <J> 0.001 </J>
            </inertia>
        </winch>
        <gearbox>
            <ratio>
                <i> 12 </i>
            </ratio>
            <inertia>
                <m> 0.1 </m>
                <J> 0.001 </J>
            </inertia>
        </gearbox>
        <motor>
            <max_torque> 50 </max_torque>
            <inertia>
                <J> 0.005 </J>
            </inertia>
        </motor>
    </drive_train>
</frame>
```

## XML-Structure - platform

```xml
<platform>
    <motion_pattern> "3R3T" </motion_pattern>
    <spatiality> "true" </spatiality>
    <body_type> "" </body_type>
    <anchors>
      <anchor>
        <id> 0 </id>
        <position>
            <x> 0 </x>
            <y> 0 </y>
            <z> 0 </z>
        <orientation>
            <R11> 1 </R11>
            <R12> 0 </R12>
            <R13> 0 </R13>
            <R21> 0 </R21>
            <R22> 1 </R22>
            <R23> 0 </R23>
            <R31> 0 </R31>
            <R32> 0 </R32>
            <R33> 1 </R33>
        </orientation>
      </anchor>
    </anchors>
    <inertia>
        <m> 0.1 </m>
        <J> 0.001 </J>
    </inertia>
    <cocs>
      <position>
        <x> 0 </x>
        <y> 0 </y>
        <z> 0 </z>
      </position>
      <orientation>
            <R11> 1 </R11>
            <R12> 0 </R12>
            <R13> 0 </R13>
            <R21> 0 </R21>
            <R22> 1 </R22>
            <R23> 0 </R23>
            <R31> 0 </R31>
            <R32> 0 </R32>
            <R33> 1 </R33>
      </orientation>
    </cocs>
</platform>
```

## XML-Structure - connectivity

```xml
<connectivity>
    <chains>
        <frame>
            <c0> 0 </c0>
            <c1> 1 </c1>
            <c2> 2 </c2>
            <c3> 3 </c3>
            <c4> 4 </c4>
            <c5> 5 </c5>
            <c6> 6 </c6>
            <c7> 7 </c7>
        </frame>
        <platform>
            <id> 0 </id>
            <c0> 0 </c0>
            <c1> 1 </c1>
            <c2> 2 </c2>
            <c3> 3 </c3>
            <c4> 4 </c4>
            <c5> 5 </c5>
            <c6> 6 </c6>
            <c7> 7 </c7>
        </platform>
    </chains>
    <platform>
    </platform>
</connectivity>
```

## XML-Structure - cables

```xml
<cables>
    <cable>
        <id> 0 </id>
        <type> "standard" </type>
        <breaking_load> 10000 </breaking_load>
    </cable>
    <cable>
        <id> 1 </id>
        <type> "standard" </type>
        <breaking_load> 10000 </breaking_load>
    </cable>
</cables>
```
