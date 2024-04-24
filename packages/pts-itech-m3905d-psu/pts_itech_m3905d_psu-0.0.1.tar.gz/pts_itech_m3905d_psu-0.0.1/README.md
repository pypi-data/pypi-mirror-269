# ITech M3905D PSU


## Description
This is an interface library for the ITech M3905D Power Supply (10V - 510A)

## Installation

`pip install pts-itech-m3905d-psu`


## Usage

### Driver Functions


<p><code class="docutils literal notranslate"><span class="pre">Base</span> <span class="pre">class</span> <span class="pre">for</span> <span class="pre">the</span> <span class="pre">ITech</span> <span class="pre">M3905D</span> <span class="pre">PSU</span></code></p>
<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.open_connection">
<span class="sig-name descname"><span class="pre">open_connection</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.open_connection" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Opens</span> <span class="pre">a</span> <span class="pre">TCP/IP</span> <span class="pre">connection</span> <span class="pre">to</span> <span class="pre">the</span> <span class="pre">ITech</span> <span class="pre">M3905D</span> <span class="pre">PSU</span></code></p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.close_connection">
<span class="sig-name descname"><span class="pre">close_connection</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.close_connection" title="Permalink to this definition"></a></dt>
<dd><p><code class="docutils literal notranslate"><span class="pre">Closes</span> <span class="pre">the</span> <span class="pre">TCP/IP</span> <span class="pre">connection</span> <span class="pre">to</span> <span class="pre">the</span> <span class="pre">ITech</span> <span class="pre">M3905D</span> <span class="pre">PSU</span></code></p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.identity">
<span class="sig-name descname"><span class="pre">identity</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.identity" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the IDN of the device.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.scpi_version">
<span class="sig-name descname"><span class="pre">scpi_version</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.scpi_version" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the version number of the used SCPI command.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.reset">
<span class="sig-name descname"><span class="pre">reset</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.reset" title="Permalink to this definition"></a></dt>
<dd><p>Resets the instrument to pre-defined values that are either typical or safe.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.system_remote">
<span class="sig-name descname"><span class="pre">system_remote</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.system_remote" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the instrument to the remote control mode via the communication interface.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.system_local">
<span class="sig-name descname"><span class="pre">system_local</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.system_local" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the instrument to local mode, i.e. panel control mode.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.system_error">
<span class="sig-name descname"><span class="pre">system_error</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.system_error" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the error information of the instrument.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.system_clear_error_queue">
<span class="sig-name descname"><span class="pre">system_clear_error_queue</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.system_clear_error_queue" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to clear the error queue.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_ip_address">
<span class="sig-name descname"><span class="pre">get_ip_address</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_ip_address" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the IP address of the instrument.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_subnetmask">
<span class="sig-name descname"><span class="pre">get_subnetmask</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_subnetmask" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the subnet mask of the LAN communication.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.selftest">
<span class="sig-name descname"><span class="pre">selftest</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">bool</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.selftest" title="Permalink to this definition"></a></dt>
<dd><p>Self-test query. Performs an instrument self-test. If self-test fails, one or more error messages will provide additional information.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>True or False</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_mode">
<span class="sig-name descname"><span class="pre">set_mode</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">mode</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Literal</span><span class="p"><span class="pre">[</span></span><span class="s"><span class="pre">'VOLT'</span></span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="s"><span class="pre">'CURR'</span></span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_mode" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the working mode of the power supply.</p>
<p>VOLTage: Indicates that the power supply is operating in CV priority mode</p>
<p>CURRent: Indicates that the power supply is operating in CC priority mode</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>mode</strong> – ‘VOLT’ or ‘CURR’</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_mode">
<span class="sig-name descname"><span class="pre">get_mode</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_mode" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the working mode of the power supply.</p>
<dl class="field-list simple">
<dt class="field-odd">Returns</dt>
<dd class="field-odd"><p>‘VOLTage’ or ‘CURRent’</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_voltage">
<span class="sig-name descname"><span class="pre">set_voltage</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">voltage</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_voltage" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the output voltage value Vset in CV priority mode</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>voltage</strong> – MINimum|MAXimum|DEFault|&lt;value&gt; ; Setting range: MIN to MAX; value: 0-10V</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_voltage">
<span class="sig-name descname"><span class="pre">get_voltage</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_voltage" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the output voltage value Vset in CV priority mode.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_current">
<span class="sig-name descname"><span class="pre">set_current</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">current</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_current" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the output current value Iset in CC priority mode</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>range</strong> (<em>current:MINimum</em><em>|</em><em>MAXimum</em><em>|</em><em>DEFault</em><em>|</em><em>&lt;value&gt; ; Setting</em>) – MIN to MAX; value: 0-510A</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_current">
<span class="sig-name descname"><span class="pre">get_current</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_current" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the output current value Iset in CC priority mode</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.output_on">
<span class="sig-name descname"><span class="pre">output_on</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.output_on" title="Permalink to this definition"></a></dt>
<dd><p>Enable the output.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.output_off">
<span class="sig-name descname"><span class="pre">output_off</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.output_off" title="Permalink to this definition"></a></dt>
<dd><p>Disable the output.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.output_status">
<span class="sig-name descname"><span class="pre">output_status</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">str</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.output_status" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the status of the output: enabled or disabled.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_voltage_upper_limit">
<span class="sig-name descname"><span class="pre">set_voltage_upper_limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">voltage_ul</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_voltage_upper_limit" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the voltage upper limit value Vlim in CC priority mode</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>voltage_ul</strong> – MINimum|MAXimum|DEFault|&lt;value&gt;; value: 0-10V; Setting range: MIN to MAX</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_voltage_lower_limit">
<span class="sig-name descname"><span class="pre">set_voltage_lower_limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">voltage_ll</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_voltage_lower_limit" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the voltage lower limit value Vl in CC priority mode</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>voltage_ll</strong> – MINimum|MAXimum|DEFault|&lt;value&gt;; value: 0-10V; Setting range: MIN to MAX</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_voltage_limits">
<span class="sig-name descname"><span class="pre">get_voltage_limits</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Tuple</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_voltage_limits" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the voltage upper limit value Vlim and voltage lower limit value Vl in CC priority mode.</p>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_current_upper_limit">
<span class="sig-name descname"><span class="pre">set_current_upper_limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">curr_ul</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_current_upper_limit" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the current upper limit value Ilim value in CV priority mode</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>curr_ul</strong> – MINimum|MAXimum|DEFault|&lt;value&gt;; value: 0-510A; Setting range: MIN to MAX</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_current_lower_limit">
<span class="sig-name descname"><span class="pre">set_current_lower_limit</span></span><span class="sig-paren">(</span><em class="sig-param"><span class="n"><span class="pre">curr_ll</span></span><span class="p"><span class="pre">:</span></span><span class="w"> </span><span class="n"><span class="pre">Union</span><span class="p"><span class="pre">[</span></span><span class="pre">float</span><span class="p"><span class="pre">,</span></span><span class="w"> </span><span class="pre">str</span><span class="p"><span class="pre">]</span></span></span></em><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">None</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.set_current_lower_limit" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to set the current lower limit value I- in CV priority mode</p>
<dl class="field-list simple">
<dt class="field-odd">Parameters</dt>
<dd class="field-odd"><p><strong>curr_ll</strong> – MINimum|MAXimum|DEFault|&lt;value&gt; ; value: 0-510A; Setting range: MIN to MAX</p>
</dd>
</dl>
</dd></dl>

<dl class="py method">
<dt class="sig sig-object py" id="pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_current_limits">
<span class="sig-name descname"><span class="pre">get_current_limits</span></span><span class="sig-paren">(</span><span class="sig-paren">)</span> <span class="sig-return"><span class="sig-return-icon">&#x2192;</span> <span class="sig-return-typehint"><span class="pre">Tuple</span></span></span><a class="headerlink" href="#pts_itech_m3905d_psu.pts_itech_m3905d_psu.ITechM3905DPSU.get_current_limits" title="Permalink to this definition"></a></dt>
<dd><p>This command is used to query the current upper limit value Ilim and current lower limit value I- in CV priority mode.</p>
</dd></dl>

</dd></dl>

</section>

## Authors and acknowledgment
Author: @shuparnadeb_pts

Maintainers: @julianpass and @shuparnadeb_pts

## License
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)



## Project status
Not in active maintenance